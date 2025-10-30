"""Module for setting up the application logger."""

from loguru import logger

from src.constants.path import Files


def setup_logger() -> None:
    """Set up the application logger."""
    log_path = Files.LOG_PATH
    logger.add(
        log_path,
        rotation="1 week",
        retention="1 month",
        level="INFO",
    )
