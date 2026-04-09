from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, require_admin
from app.schemas import AdminStatsRead, AuditLogRead
from app.services.audit_service import AdminStatsService, AuditService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsRead)
def admin_stats(_: object = Depends(require_admin), db: Session = Depends(get_db_session)):
    return AdminStatsService(db).stats()


@router.get("/audit-logs", response_model=list[AuditLogRead])
def admin_audit_logs(
    _: object = Depends(require_admin),
    guild_id: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db_session),
):
    return AuditService(db).list_logs(guild_id=guild_id, limit=limit)
