from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.core.dependencies import get_current_user, get_db_session
from app.core.jwt_utils import InvalidOAuthStateError, create_oauth_state, verify_oauth_state
from app.models import User
from app.schemas import (
    AuthTokens,
    DiscordLoginResponse,
    LogoutAllResponse,
    MeResponse,
    RefreshSessionRequest,
    SessionRead,
    UserRead,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_auth_cookies(response: Response, tokens: dict) -> None:
    response.set_cookie(
        "access_token",
        tokens["access_token"],
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.jwt_access_ttl_minutes * 60,
    )
    response.set_cookie(
        "refresh_token",
        tokens["refresh_token"],
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.jwt_refresh_ttl_days * 86400,
    )
    response.set_cookie(
        "session_id",
        tokens["session_id"],
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.jwt_refresh_ttl_days * 86400,
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access_token", domain=settings.cookie_domain)
    response.delete_cookie("refresh_token", domain=settings.cookie_domain)
    response.delete_cookie("session_id", domain=settings.cookie_domain)


@router.get("/login", response_model=DiscordLoginResponse)
def login(response: Response, db: Session = Depends(get_db_session)):
    state = create_oauth_state()
    response.set_cookie(
        "oauth_state",
        state,
        httponly=True,
        max_age=600,
        samesite=settings.cookie_samesite,
        secure=settings.cookie_secure,
    )
    return {"auth_url": AuthService(db).discord_auth_url(state)}


@router.get("/callback")
async def callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db_session),
):
    cookie_state = request.cookies.get("oauth_state")
    if not cookie_state or cookie_state != state:
        raise HTTPException(status_code=400, detail="OAuth state mismatch")
    try:
        verify_oauth_state(state)
    except InvalidOAuthStateError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    service = AuthService(db)
    _, user_data = await service.exchange_code(code)
    result = service.finalize_login(user_data, request.client.host if request.client else None, request.headers.get("user-agent"))

    response = RedirectResponse(f"{settings.frontend_url}/dashboard", status_code=302)
    response.delete_cookie("oauth_state")
    _set_auth_cookies(response, result)
    return response


@router.post("/refresh", response_model=AuthTokens)
def refresh_session(payload: RefreshSessionRequest, request: Request, response: Response, db: Session = Depends(get_db_session)):
    refresh_token = payload.refresh_token or request.cookies.get("refresh_token")
    session_id = request.cookies.get("session_id")
    if not refresh_token or not session_id:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    tokens = AuthService(db).refresh_session(session_id=session_id, refresh_token=refresh_token)
    _set_auth_cookies(response, tokens)
    return {**tokens, "token_type": "bearer"}


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db_session)):
    sid = request.cookies.get("session_id")
    if sid:
        AuthService(db).logout(sid)
    _clear_auth_cookies(response)
    return {"ok": True}


@router.post("/logout-all", response_model=LogoutAllResponse)
def logout_all(user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    revoked = AuthService(db).logout_all(user_id=user.id)
    return {"revoked_sessions": revoked}


@router.get("/me", response_model=MeResponse)
def me(request: Request, user: User = Depends(get_current_user)):
    return {
        "user": UserRead.model_validate(user),
        "session": SessionRead(
            session_id=getattr(request.state, "session_id", ""),
            expires_at=getattr(request.state, "session_expires_at", user.updated_at),
        ),
    }


router.add_api_route("/discord/login", login, methods=["GET"], response_model=DiscordLoginResponse)
router.add_api_route("/discord/callback", callback, methods=["GET"])
