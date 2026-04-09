from __future__ import annotations

from datetime import datetime
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from shared.config import get_settings
from shared.date_utils import add_days, add_minutes, utcnow
from shared.exceptions import AuthError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    now = utcnow()
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(add_minutes(now, settings.jwt_access_ttl_minutes).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, session_id: str, extra_claims: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    now = utcnow()
    payload: dict[str, Any] = {
        "sub": subject,
        "sid": session_id,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(add_days(now, settings.jwt_refresh_ttl_days).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise AuthError("Invalid token") from exc
    return payload


def token_expiry(token_payload: dict[str, Any]) -> datetime:
    exp = token_payload.get("exp")
    if not isinstance(exp, int):
        raise AuthError("Token payload missing exp")
    return datetime.fromtimestamp(exp, tz=utcnow().tzinfo)
