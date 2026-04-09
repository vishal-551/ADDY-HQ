from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate


class TaskService:
    """Encapsulates task persistence and business rules."""

    def __init__(self, session: Session):
        self.session = session

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        query = select(Task).order_by(Task.created_at.desc())
        if status:
            query = query.where(Task.status == status)
        return list(self.session.scalars(query).all())

    def get_task(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def create_task(self, payload: TaskCreate) -> Task:
        task = Task(
            title=payload.title.strip(),
            description=payload.description.strip(),
            owner=payload.owner.strip(),
            priority=payload.priority,
        )
        self.session.add(task)
        self.session.flush()
        self.session.refresh(task)
        return task

    def bulk_create(self, payloads: Iterable[TaskCreate]) -> list[Task]:
        records = [
            Task(
                title=p.title.strip(),
                description=p.description.strip(),
                owner=p.owner.strip(),
                priority=p.priority,
            )
            for p in payloads
        ]
        self.session.add_all(records)
        self.session.flush()
        return records

    def update_task(self, task: Task, payload: TaskUpdate) -> Task:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.session.add(task)
        self.session.flush()
        self.session.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.session.delete(task)
        self.session.flush()
