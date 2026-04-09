from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.jwt_utils import InvalidTokenError
from app.core.request_context import get_request_id
from shared.response_builder import error
from shared.exceptions import AppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=error(
                "validation_error",
                "Request validation failed",
                details={"errors": exc.errors(), "request_id": get_request_id()},
            ),
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(_: Request, exc: InvalidTokenError):
        payload = error("invalid_token", str(exc), details={"request_id": get_request_id()})
        return JSONResponse(status_code=401, content=payload)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        detail = exc.detail
        if isinstance(detail, dict):
            payload = detail
            if "ok" not in payload:
                payload = error("http_error", "Request failed", details={"detail": detail, "request_id": get_request_id()})
        else:
            payload = error("http_error", str(detail), details={"request_id": get_request_id()})
        return JSONResponse(status_code=exc.status_code, content=payload, headers=exc.headers)

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        payload = exc.to_dict()
        details = payload.setdefault("error", {}).setdefault("details", {})
        details["request_id"] = get_request_id()
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_handler(_: Request, __: Exception):
        payload = error("internal_error", "Internal server error", details={"request_id": get_request_id()})
        return JSONResponse(status_code=500, content=payload)
