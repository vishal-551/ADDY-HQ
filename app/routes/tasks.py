from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from app.database import get_session
from app.models import TaskCreate, TaskRead, TaskStatus, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(status_filter: TaskStatus | None = Query(default=None, alias="status")):
    with get_session() as session:
        service = TaskService(session)
        return service.list_tasks(status_filter)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    with get_session() as session:
        service = TaskService(session)
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    with get_session() as session:
        service = TaskService(session)
        return service.create_task(payload)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate):
    with get_session() as session:
        service = TaskService(session)
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return service.update_task(task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_session() as session:
        service = TaskService(session)
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        service.delete_task(task)
