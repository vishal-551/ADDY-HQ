from __future__ import annotations

from contextvars import ContextVar


audit_context_var: ContextVar[dict] = ContextVar("audit_context", default={})
