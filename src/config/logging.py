"""Module for setting up the application logger."""

from loguru import logger

from . import settings


def setup_logger() -> None:
    """Set up the application logger."""
    log_path = settings.LOGS_DIR / "log.log"
    logger.add(
        log_path,
        rotation="1 week",
        retention="1 month",
        level="INFO",
    )
