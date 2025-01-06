"""Точка входа в приложение Take Break."""

import sys
from pathlib import Path

# Добавляем путь к пакету в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from take_break.__main__ import setup_logger
from take_break.app import TakeBreakApp


def main() -> None:
    """Точка входа в приложение."""
    setup_logger()
    app = TakeBreakApp()
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
