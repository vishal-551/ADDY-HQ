from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.core.dependencies import get_current_user, get_db_session
from app.models import User
from app.schemas import DiscordLoginResponse, MeResponse, SessionRead, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", response_model=DiscordLoginResponse)
def login(response: Response, db: Session = Depends(get_db_session)):
    state = secrets.token_urlsafe(24)
    response.set_cookie("oauth_state", state, httponly=True, max_age=600, samesite=settings.cookie_samesite)
    return {"auth_url": AuthService(db).discord_auth_url(state)}


@router.get("/callback")
async def callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db_session),
):
    cookie_state = request.cookies.get("oauth_state")
    if cookie_state != state:
        raise HTTPException(status_code=400, detail="OAuth state mismatch")

    service = AuthService(db)
    _, user_data = await service.exchange_code(code)
    result = service.finalize_login(user_data, request.client.host if request.client else None, request.headers.get("user-agent"))

    response = RedirectResponse(f"{settings.frontend_url}/dashboard", status_code=302)
    response.delete_cookie("oauth_state")
    for key in ("access_token", "refresh_token", "session_id"):
        response.set_cookie(
            key,
            result[key],
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
        )
    return response


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db_session)):
    sid = request.cookies.get("session_id")
    if sid:
        AuthService(db).logout(sid)
    response.delete_cookie("access_token", domain=settings.cookie_domain)
    response.delete_cookie("refresh_token", domain=settings.cookie_domain)
    response.delete_cookie("session_id", domain=settings.cookie_domain)
    return {"ok": True}


@router.get("/me", response_model=MeResponse)
def me(request: Request, user: User = Depends(get_current_user)):
    return {
        "user": UserRead.model_validate(user),
        "session": SessionRead(session_id=getattr(request.state, "session_id", ""), expires_at=user.updated_at),
    }


# Backward-compatible aliases from previous route names.
router.add_api_route("/discord/login", login, methods=["GET"], response_model=DiscordLoginResponse)
router.add_api_route("/discord/callback", callback, methods=["GET"])
