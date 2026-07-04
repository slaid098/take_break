"""Управление автозапуском приложения в Windows."""

import sys
from pathlib import Path
from typing import Any

from loguru import logger

try:
    import winreg as _winreg

    winreg: Any = _winreg
except ImportError:
    winreg: Any = None  # type: ignore[no-redef]

_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_APP_NAME = "TakeBreak"


def get_exe_path() -> str | None:
    """Получить путь к исполняемому файлу.

    Returns:
        Путь к .exe файлу, или None если запущено как Python-скрипт.

    """
    if not getattr(sys, "frozen", False):
        return None
    return str(Path(sys.executable).resolve())


def is_autostart_enabled() -> bool:
    """Проверить, включён ли автозапуск в реестре Windows.

    Returns:
        True если автозапуск включён, False иначе.

    """
    if winreg is None:
        logger.debug("Автозапуск недоступен на этой платформе")
        return False

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY)
    except OSError as e:
        logger.error(f"Не удалось открыть ключ реестра: {e}")
        return False

    try:
        winreg.QueryValueEx(key, _APP_NAME)
    except FileNotFoundError:
        return False
    else:
        return True
    finally:
        winreg.CloseKey(key)


def enable_autostart() -> None:
    """Включить автозапуск через реестр Windows.

    Работает только для скомпилированного .exe файла.
    """
    if winreg is None:
        logger.warning("Автозапуск недоступен на этой платформе")
        return

    exe_path = get_exe_path()
    if exe_path is None:
        logger.warning("Автозапуск доступен только для скомпилированного приложения")
        return

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            _RUN_KEY,
            0,
            winreg.KEY_SET_VALUE,
        )
    except OSError as e:
        logger.error(f"Не удалось открыть ключ реестра: {e}")
        return

    try:
        winreg.SetValueEx(key, _APP_NAME, 0, winreg.REG_SZ, exe_path)
        logger.info("Автозапуск включён")
    finally:
        winreg.CloseKey(key)


def disable_autostart() -> None:
    """Отключить автозапуск, удалив запись из реестра Windows."""
    if winreg is None:
        logger.warning("Автозапуск недоступен на этой платформе")
        return

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            _RUN_KEY,
            0,
            winreg.KEY_SET_VALUE,
        )
    except FileNotFoundError:
        logger.debug("Запись автозапуска не найдена, нечего удалять")
        return
    except OSError as e:
        logger.error(f"Не удалось открыть ключ реестра: {e}")
        return

    try:
        winreg.DeleteValue(key, _APP_NAME)
        logger.info("Автозапуск отключён")
    except FileNotFoundError:
        logger.debug("Запись автозапуска не найдена, нечего удалять")
    finally:
        winreg.CloseKey(key)
