from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.jwt_utils import InvalidTokenError
from shared.exceptions import AppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "error": {"code": "validation_error", "message": "Request validation failed", "details": exc.errors()},
            },
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(_: Request, exc: InvalidTokenError):
        return JSONResponse(status_code=401, content={"ok": False, "error": {"code": "invalid_token", "message": str(exc)}})

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(Exception)
    async def unhandled_handler(_: Request, __: Exception):
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": {"code": "internal_error", "message": "Internal server error"}},
        )
