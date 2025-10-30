"""Точка входа в приложение Take Break."""

import sys

from loguru import logger

from src.app import App
from src.config.logger import setup_logger
from src.constants.path import Directories


def main() -> None:
    """Run the Take Break application.

    Initializes the logger, creates an application instance, runs the
    main loop, and handles graceful shutdown on KeyboardInterrupt
    or unexpected errors.
    """
    Directories().make_dirs()
    setup_logger()
    logger.info("Запуск приложения Take Break")

    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Приложение остановлено пользователем")
        app.quit()
    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
    finally:
        logger.info("Завершение работы приложения")
        sys.exit(0)


if __name__ == "__main__":
    main()
