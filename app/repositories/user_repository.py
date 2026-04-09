from __future__ import annotations

from app.repositories.users_repository import UsersRepository


class UserRepository(UsersRepository):
    """Backward-compatible singular repository alias used by service-layer wiring."""

    pass
