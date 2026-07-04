"""Точка входа в приложение Take Break."""

import sys

from loguru import logger

from src.app import App
from src.config.logger import setup_logger
from src.constants.path import Directories


def main() -> None:
    """Запустить приложение Take Break.

    Инициализирует логгер, создаёт экземпляр приложения,
    запускает главный цикл и обрабатывает корректное завершение
    при KeyboardInterrupt или неожиданных ошибках.
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
        import keyboard

        keyboard.unhook_all()
        logger.info("Завершение работы приложения")
        sys.exit(0)


if __name__ == "__main__":
    main()