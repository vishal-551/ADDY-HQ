from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Any


@dataclass(slots=True)
class AppError(Exception):
    code: str
    message: str
    status_code: int = HTTPStatus.BAD_REQUEST
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details or {},
            },
        }


class AuthError(AppError):
    def __init__(self, message: str = "Unauthorized", details: dict[str, Any] | None = None):
        super().__init__("auth_error", message, HTTPStatus.UNAUTHORIZED, details)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden", details: dict[str, Any] | None = None):
        super().__init__("forbidden", message, HTTPStatus.FORBIDDEN, details)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not Found", details: dict[str, Any] | None = None):
        super().__init__("not_found", message, HTTPStatus.NOT_FOUND, details)


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed", details: dict[str, Any] | None = None):
        super().__init__("validation_error", message, HTTPStatus.UNPROCESSABLE_ENTITY, details)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflict", details: dict[str, Any] | None = None):
        super().__init__("conflict", message, HTTPStatus.CONFLICT, details)


class RateLimitedError(AppError):
    def __init__(self, message: str = "Too many requests", details: dict[str, Any] | None = None):
        super().__init__("rate_limited", message, HTTPStatus.TOO_MANY_REQUESTS, details)
