from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_session
from app.services.task_service import TaskService

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/dashboard/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    with get_session() as session:
        service = TaskService(session)
        tasks = service.list_tasks()

    status_counts = Counter(task.status.value for task in tasks)
    priority_counts = Counter(task.priority.value for task in tasks)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "tasks": tasks,
            "status_counts": dict(status_counts),
            "priority_counts": dict(priority_counts),
            "total": len(tasks),
        },
    )
