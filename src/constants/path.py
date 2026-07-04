"""Константы путей приложения."""

import sys
from dataclasses import dataclass, fields
from pathlib import Path


def get_base_dir() -> Path:
    """Получить базовую директорию приложения.

    Returns:
        Для .exe: директория где находится .exe.
        Для скрипта: корневая директория проекта.

    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent.parent


@dataclass(slots=True)
class Directories:
    """Директории приложения."""

    APP_DATA_DIR = get_base_dir() / "app_data"
    LOGS_DIR = APP_DATA_DIR / "logs"
    WALLPAPERS_DIR = APP_DATA_DIR / "wallpapers"
    CACHE_DIR = APP_DATA_DIR / "cache"
    LOGO_DIR = APP_DATA_DIR / "icon"
    SETTINGS_DIR = APP_DATA_DIR / "settings"

    @property
    def base_dir(self) -> Path:
        """Получить базовую директорию приложения.

        Returns:
            Для .exe: директория где находится .exe.
            Для скрипта: корневая директория проекта.

        """
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent
        return Path(__file__).parent.parent.parent

    def make_dirs(self) -> None:
        """Создать все необходимые директории приложения."""
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class Files:
    """Файлы приложения."""

    LOGO_PATH = Directories.LOGO_DIR / "icon.ico"
    SETTINGS_DB_PATH = Directories.SETTINGS_DIR / "settings.db"
    WALLPAPER_CACHE_PATH = Directories.CACHE_DIR / "wallpaper_cache.jpg"
    LOG_PATH = Directories.LOGS_DIR / "log.log"
    MEMORY_DB_PATH = ":memory:"
