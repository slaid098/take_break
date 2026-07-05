"""Константы путей приложения."""

import sys
from pathlib import Path


def get_base_dir() -> Path:
    """Получить директорию пользовательских данных (read-write).

    Returns:
        Для .exe: директория где находится .exe (создаётся рядом).
        Для скрипта: корневая директория проекта.

    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent.parent


def get_bundle_dir() -> Path:
    """Получить директорию упакованных ресурсов (read-only).

    Returns:
        Для .exe: sys._MEIPASS (внутренняя директория PyInstaller).
        Для скрипта: корневая директория проекта.

    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).parent.parent.parent


class Directories:
    """Директории приложения.

    Read-only ресурсы (иконка, обои) — из bundle (sys._MEIPASS).
    User data (БД, логи, кэш) — рядом с exe (persist между обновлениями).
    """

    LOGS_DIR: Path = get_base_dir() / "app_data" / "logs"
    CACHE_DIR: Path = get_base_dir() / "app_data" / "cache"
    SETTINGS_DIR: Path = get_base_dir() / "app_data" / "settings"
    LOGO_DIR: Path = get_bundle_dir() / "app_data" / "logo"
    WALLPAPERS_DIR: Path = get_bundle_dir() / "app_data" / "wallpapers"

    def make_dirs(self) -> None:
        """Создать все необходимые директории пользователя."""
        for value in vars(type(self)).values():
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)


class Files:
    """Файлы приложения."""

    LOGO_PATH: Path = Directories.LOGO_DIR / "logo.ico"
    SETTINGS_DB_PATH: Path = Directories.SETTINGS_DIR / "settings.db"
    WALLPAPER_CACHE_PATH: Path = Directories.CACHE_DIR / "wallpaper_cache.jpg"
    LOG_PATH: Path = Directories.LOGS_DIR / "log.log"
    MEMORY_DB_PATH: str = ":memory:"
