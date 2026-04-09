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


@router.get("/discord/login", response_model=DiscordLoginResponse)
def discord_login(response: Response, db: Session = Depends(get_db_session)):
    state = secrets.token_urlsafe(24)
    response.set_cookie("oauth_state", state, httponly=True, max_age=600, samesite="lax")
    url = AuthService(db).discord_auth_url(state)
    return {"auth_url": url}


@router.get("/discord/callback")
async def discord_callback(
    request: Request,
    response: Response,
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
    response.set_cookie("access_token", result["access_token"], httponly=True, samesite="lax")
    response.set_cookie("refresh_token", result["refresh_token"], httponly=True, samesite="lax")
    response.set_cookie("session_id", result["session_id"], httponly=True, samesite="lax")
    return response


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db_session)):
    sid = request.cookies.get("session_id")
    if sid:
        AuthService(db).logout(sid)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("session_id")
    return {"ok": True}


@router.get("/me", response_model=MeResponse)
def me(request: Request, user: User = Depends(get_current_user)):
    return {
        "user": UserRead(
            id=user.id,
            discord_id=user.discord_id,
            username=user.username,
            avatar=user.avatar,
            is_admin=user.is_admin,
        ),
        "session": SessionRead(session_id=getattr(request.state, "session_id", ""), expires_at=user.updated_at),
    }
