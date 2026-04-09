from __future__ import annotations

from typing import Any


def ok(data: Any = None, *, message: str | None = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": True, "data": data}
    if message:
        payload["message"] = message
    if meta:
        payload["meta"] = meta
    return payload


def error(code: str, message: str, *, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }
