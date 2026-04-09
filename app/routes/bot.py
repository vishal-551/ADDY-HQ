from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.database import get_session
from app.services.bot_service import TaskBotService

router = APIRouter(prefix="/bot", tags=["bot"])


class BotCommandRequest(BaseModel):
    command: str = Field(min_length=3, max_length=500)


@router.post("/command")
def run_command(payload: BotCommandRequest):
    with get_session() as session:
        bot = TaskBotService(session)
        result = bot.execute(payload.command)
        return result
