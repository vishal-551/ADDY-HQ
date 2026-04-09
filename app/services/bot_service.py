from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import TaskPriority, TaskStatus
from app.schemas import TaskCreate, TaskUpdate
from app.services.task_service import TaskService


@dataclass(frozen=True)
class BotDecision:
    intent: str
    confidence: float


class TaskBotService:
    """Simple command bot for operations teams.

    Supported commands:
    - create <owner> | <title> | <description>
    - complete <id>
    - escalate <id>
    """

    def __init__(self, session: Session):
        self.task_service = TaskService(session)

    def classify(self, command: str) -> BotDecision:
        normalized = command.strip().lower()
        if normalized.startswith("create "):
            return BotDecision("create", 0.98)
        if normalized.startswith("complete "):
            return BotDecision("complete", 0.95)
        if normalized.startswith("escalate "):
            return BotDecision("escalate", 0.96)
        return BotDecision("unknown", 0.0)

    def execute(self, command: str) -> dict:
        decision = self.classify(command)
        if decision.intent == "create":
            return self._create_from_command(command)
        if decision.intent == "complete":
            return self._complete_from_command(command)
        if decision.intent == "escalate":
            return self._escalate_from_command(command)
        return {"ok": False, "message": "Unsupported command"}

    def _create_from_command(self, command: str) -> dict:
        body = command[len("create ") :].strip()
        segments = [part.strip() for part in body.split("|")]
        if len(segments) < 2:
            return {"ok": False, "message": "Format: create <owner> | <title> | <description>"}

        owner, title = segments[0], segments[1]
        description = segments[2] if len(segments) > 2 else ""
        task = self.task_service.create_task(
            TaskCreate(owner=owner, title=title, description=description, priority=TaskPriority.medium)
        )
        return {"ok": True, "message": "Task created", "task_id": task.id}

    def _complete_from_command(self, command: str) -> dict:
        task_id_str = command[len("complete ") :].strip()
        if not task_id_str.isdigit():
            return {"ok": False, "message": "Task ID must be a number"}
        task = self.task_service.get_task(int(task_id_str))
        if not task:
            return {"ok": False, "message": "Task not found"}
        self.task_service.update_task(task, TaskUpdate(status=TaskStatus.completed))
        return {"ok": True, "message": "Task completed", "task_id": task.id}

    def _escalate_from_command(self, command: str) -> dict:
        task_id_str = command[len("escalate ") :].strip()
        if not task_id_str.isdigit():
            return {"ok": False, "message": "Task ID must be a number"}
        task = self.task_service.get_task(int(task_id_str))
        if not task:
            return {"ok": False, "message": "Task not found"}
        self.task_service.update_task(task, TaskUpdate(priority=TaskPriority.high, status=TaskStatus.in_progress))
        return {"ok": True, "message": "Task escalated", "task_id": task.id}
