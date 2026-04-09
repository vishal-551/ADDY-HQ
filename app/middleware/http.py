from __future__ import annotations

import time
from collections import defaultdict, deque
from datetime import UTC, datetime

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = f"req_{int(time.time() * 1000)}"
        request.state.request_id = request_id
        request.state.started_at = datetime.now(UTC)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
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
            return JSONResponse(
                {"ok": False, "error": {"code": "rate_limited", "message": "Too many requests"}}, status_code=429
            )
        bucket.append(now)
        return await call_next(request)


class AuditContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.audit_context = {
            "request_id": getattr(request.state, "request_id", f"req_{int(time.time() * 1000)}"),
            "path": request.url.path,
            "method": request.method,
            "ip": request.client.host if request.client else None,
            "started_at": datetime.now(UTC).isoformat(),
        }
        return await call_next(request)
