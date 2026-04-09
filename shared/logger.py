from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from shared.config import get_settings


_INITIALIZED = False


def configure_logging() -> None:
    global _INITIALIZED
    if _INITIALIZED:
        return

    settings = get_settings()

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.log_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )

    _INITIALIZED = True


def get_logger(name: str = "addy") -> structlog.stdlib.BoundLogger:
    configure_logging()
    return structlog.get_logger(name)
