from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.config import settings
from shared.security import hash_password, verify_password


class InvalidTokenError(Exception):
    pass


class InvalidOAuthStateError(Exception):
    pass


def utcnow() -> datetime:
    return datetime.now(UTC)


def create_access_token(subject: str, session_id: str, claims: dict[str, Any] | None = None) -> str:
    now = utcnow()
    payload: dict[str, Any] = {
        "sub": subject,
        "sid": session_id,
        "typ": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_access_ttl_minutes)).timestamp()),
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, session_id: str) -> str:
    now = utcnow()
    payload = {
        "sub": subject,
        "sid": session_id,
        "typ": "refresh",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=settings.jwt_refresh_ttl_days)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise InvalidTokenError("Invalid or expired token") from exc


def generate_session_id() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return hash_password(digest)


def verify_token_hash(raw_token: str, hashed_token: str) -> bool:
    digest = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    return verify_password(digest, hashed_token)


def create_oauth_state(ttl_seconds: int = 600) -> str:
    issued_at = int(utcnow().timestamp())
    nonce = secrets.token_urlsafe(18)
    raw = f"{issued_at}.{ttl_seconds}.{nonce}"
    sig = hmac.new(settings.jwt_secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{raw}.{sig}"


def verify_oauth_state(state: str) -> None:
    try:
        issued_at_raw, ttl_raw, nonce, sig = state.split(".", 3)
    except ValueError as exc:
        raise InvalidOAuthStateError("OAuth state is malformed") from exc

    raw = f"{issued_at_raw}.{ttl_raw}.{nonce}"
    expected_sig = hmac.new(settings.jwt_secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, sig):
        raise InvalidOAuthStateError("OAuth state signature mismatch")

    issued_at = int(issued_at_raw)
    ttl_seconds = int(ttl_raw)
    if int(utcnow().timestamp()) > issued_at + ttl_seconds:
        raise InvalidOAuthStateError("OAuth state expired")
