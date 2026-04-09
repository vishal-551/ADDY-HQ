from __future__ import annotations

from collections.abc import Generator
from typing import Any
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import DateTime, MetaData, create_engine, func
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.config import settings

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class IDMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def _sqlite_connect_args(url: str) -> dict[str, bool]:
    return {"check_same_thread": False} if url.startswith("sqlite") else {}


def _engine_kwargs(url: str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"future": True}
    connect_args = _sqlite_connect_args(url)
    if connect_args:
        kwargs["connect_args"] = connect_args
    if not url.startswith("sqlite"):
        kwargs["pool_pre_ping"] = True
    return kwargs


engine = create_engine(settings.sync_database_url, **_engine_kwargs(settings.sync_database_url))
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


def _resolve_async_url() -> str:
    url = settings.database_url
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("sqlite+aiosqlite://"):
        return url
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


def _create_async_engine() -> AsyncEngine | None:
    try:
        return create_async_engine(_resolve_async_url(), **_engine_kwargs(_resolve_async_url()))
    except ModuleNotFoundError:
        return None


async_engine = _create_async_engine()
AsyncSessionLocal = (
    async_sessionmaker(bind=async_engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
    if async_engine is not None
    else None
)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def get_async_db() -> Generator[AsyncSession, None, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database driver is not installed. Configure DATABASE_URL with an async driver.")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
