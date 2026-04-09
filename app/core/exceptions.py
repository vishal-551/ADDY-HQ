from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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

    @app.exception_handler(Exception)
    async def unhandled_handler(_: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": {"code": "internal_error", "message": "Internal server error"}},
        )
