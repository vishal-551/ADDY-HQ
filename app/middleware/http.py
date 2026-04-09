from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from datetime import UTC, datetime
from uuid import uuid4

import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.core.request_context import audit_context_var, request_id_var, set_audit_context, set_request_id
from shared.response_builder import error, ok


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        request.state.request_id = request_id
        request.state.started_at = datetime.now(UTC)
        request_token = request_id_var.set(request_id)
        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(request_token)
        response.headers["X-Request-ID"] = request_id
        return response


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = structlog.get_logger("api.http")

    async def dispatch(self, request: Request, call_next):
        started_at = time.perf_counter()
        response = None
        error_type = None
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            error_type = exc.__class__.__name__
            raise
        finally:
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            self.logger.info(
                "request.complete",
                method=request.method,
                path=request.url.path,
                query=request.url.query,
                status_code=getattr(response, "status_code", 500),
                elapsed_ms=elapsed_ms,
                request_id=getattr(request.state, "request_id", None),
                client_ip=request.client.host if request.client else None,
                user_id=getattr(getattr(request.state, "user", None), "id", None),
                error_type=error_type,
            )


class ResponseEnvelopeMiddleware(BaseHTTPMiddleware):
    """Normalizes successful JSON responses to the shared {ok,data} shape."""

    _SKIP_PATH_PREFIXES = ("/docs", "/openapi.json", "/redoc")

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path.startswith(self._SKIP_PATH_PREFIXES):
            return response
        if response.status_code >= 400:
            return response
        if not isinstance(response, JSONResponse):
            return response

        media_type = response.media_type or ""
        if "application/json" not in media_type:
            return response

        raw_body = getattr(response, "body", b"")
        if not raw_body:
            return response

        try:
            parsed = json.loads(raw_body)
        except json.JSONDecodeError:
            return response

        if isinstance(parsed, dict) and "ok" in parsed:
            return response

        wrapped = ok(parsed)
        return JSONResponse(content=wrapped, status_code=response.status_code, headers=dict(response.headers))


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.window_seconds = 60
        self.max_per_window = settings.rate_limit_per_minute
        self._calls: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if not settings.enable_rate_limiting:
            return await call_next(request)

        key_parts = [request.client.host if request.client else "unknown"]
        session_id = request.cookies.get("session_id")
        if session_id:
            key_parts.append(session_id)
        key = ":".join(key_parts)

        now = time.time()
        bucket = self._calls[key]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.max_per_window:
            return JSONResponse(error("rate_limited", "Too many requests"), status_code=429)
        bucket.append(now)
        return await call_next(request)


class AuditContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.audit_context = {
            "request_id": getattr(request.state, "request_id", uuid4().hex),
            "path": request.url.path,
            "method": request.method,
            "ip": request.client.host if request.client else None,
            "started_at": datetime.now(UTC).isoformat(),
        }
        set_audit_context(request.state.audit_context)
        set_request_id(request.state.audit_context["request_id"])
        token = audit_context_var.set(request.state.audit_context)
        try:
            return await call_next(request)
        finally:
            audit_context_var.reset(token)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    logger = structlog.get_logger("api.errors")

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException:
            raise
        except Exception:  # pragma: no cover - fallback for middleware stack exceptions
            self.logger.exception("request.unhandled_exception", path=request.url.path, method=request.method)
            return JSONResponse(error("internal_error", "Internal server error"), status_code=500)
