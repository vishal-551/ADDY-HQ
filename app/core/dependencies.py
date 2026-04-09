from __future__ import annotations

from datetime import UTC, datetime

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.jwt_utils import decode_jwt
from app.database import get_db
from app.models import User
from app.repositories.auth_repository import AuthRepository
from app.services.access_service import PremiumAccessService
from app.services.audit_service import AuditService
from app.services.customer_identity_service import CustomerIdentityService
from app.services.guild_service import GuildService
from app.services.settings_service import GeneralSettingsService


def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db


def _get_access_token(request: Request, authorization: str | None) -> str:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    token = request.cookies.get("access_token")
    if token:
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth token")


def get_current_user(
    request: Request,
    db: Session = Depends(get_db_session),
    authorization: str | None = Header(default=None),
) -> User:
    token = _get_access_token(request, authorization)
    payload = decode_jwt(token)
    if payload.get("typ") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token type")

    subject = payload.get("sub")
    session_id = payload.get("sid")
    if not subject or not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")

    repo = AuthRepository(db)
    user = repo.get_user_by_discord_id(int(subject))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    now = datetime.now(UTC)
    session = repo.get_active_session(session_id, now)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or revoked")

    request.state.user = user
    request.state.session_id = session_id
    request.state.session_expires_at = session.expires_at
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.is_admin or user.discord_id in settings.admin_user_ids:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")


def get_guild_service(db: Session = Depends(get_db_session)) -> GuildService:
    return GuildService(db)


def get_settings_service(db: Session = Depends(get_db_session)) -> GeneralSettingsService:
    return GeneralSettingsService(db)


def get_premium_service(db: Session = Depends(get_db_session)) -> PremiumAccessService:
    return PremiumAccessService(db)


def get_customer_identity_service(db: Session = Depends(get_db_session)) -> CustomerIdentityService:
    return CustomerIdentityService(db)


def get_audit_service(db: Session = Depends(get_db_session)) -> AuditService:
    return AuditService(db)
