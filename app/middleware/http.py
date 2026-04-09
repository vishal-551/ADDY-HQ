from __future__ import annotations

import time
from collections import defaultdict, deque
from datetime import UTC, datetime
from uuid import uuid4

import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.core.request_context import audit_context_var, set_audit_context
from shared.response_builder import error


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        request.state.request_id = request_id
        request.state.started_at = datetime.now(UTC)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = structlog.get_logger("api.http")

    async def dispatch(self, request: Request, call_next):
        started_at = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            self.logger.info(
                "request.complete",
                method=request.method,
                path=request.url.path,
                query=request.url.query,
                status_code=getattr(locals().get("response"), "status_code", 500),
                elapsed_ms=elapsed_ms,
                request_id=getattr(request.state, "request_id", None),
                client_ip=request.client.host if request.client else None,
                user_id=getattr(getattr(request.state, "user", None), "id", None),
            )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.window_seconds = 60
        self.max_per_window = settings.rate_limit_per_minute
        self._calls: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if not settings.enable_rate_limiting:
            return await call_next(request)
        key = request.client.host if request.client else "unknown"
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
        token = audit_context_var.set(request.state.audit_context)
        try:
            return await call_next(request)
        finally:
            audit_context_var.reset(token)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException:
            raise
        except Exception:  # pragma: no cover - fallback for middleware stack exceptions
            return JSONResponse(error("internal_error", "Internal server error"), status_code=500)
