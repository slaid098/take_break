"""Точка входа в приложение Take Break."""

import sys
from pathlib import Path

from loguru import logger

from .app import TakeBreakApp


def setup_logger() -> None:
    """Настройка логирования."""
    log_path = Path.home() / "take_break.log"
    logger.add(
        log_path,
        rotation="1 week",
        retention="1 month",
        level="INFO",
    )


def main() -> None:
    """Точка входа в приложение."""
    setup_logger()
    logger.info("Запуск приложения Take Break")

    app = TakeBreakApp()
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Приложение остановлено пользователем")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
    finally:
        logger.info("Завершение работы приложения")
        sys.exit(0)


if __name__ == "__main__":
    main()
