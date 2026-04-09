from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any


audit_context_var: ContextVar[dict[str, Any]] = ContextVar("audit_context", default={})
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


@dataclass(slots=True)
class AuditActor:
    user_id: int | None
    actor_type: str


def set_audit_context(context: dict[str, Any]) -> None:
    audit_context_var.set(context)


def get_audit_context() -> dict[str, Any]:
    return audit_context_var.get()


def merge_audit_metadata(metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    base = get_audit_context().copy()
    if metadata:
        base.update(metadata)
    return base


def set_request_id(request_id: str | None) -> None:
    request_id_var.set(request_id)


def get_request_id() -> str | None:
    return request_id_var.get()
