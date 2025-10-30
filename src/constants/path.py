"""Path constants for the application."""

import sys
from dataclasses import dataclass, fields
from pathlib import Path


def get_base_dir() -> Path:
    """Get the base directory of the application.

    Returns:
        For compiled .exe: directory where .exe is located.
        For Python script: project root directory.

    """
    if getattr(sys, "frozen", False):
        # Running as compiled .exe - use .exe location
        return Path(sys.executable).parent

    # Running as script - use project root (3 levels up from this file)
    return Path(__file__).parent.parent.parent


@dataclass(slots=True)
class Directories:
    """Directories for the application."""

    APP_DATA_DIR = get_base_dir() / "app_data"
    LOGS_DIR = APP_DATA_DIR / "logs"
    WALLPAPERS_DIR = APP_DATA_DIR / "wallpapers"
    CACHE_DIR = APP_DATA_DIR / "cache"
    ICON_DIR = APP_DATA_DIR / "icon"
    SETTINGS_DIR = APP_DATA_DIR / "settings"

    @property
    def base_dir(self) -> Path:
        """Get the base directory of the application.

        Returns:
            For compiled .exe: directory where .exe is located.
            For Python script: project root directory.

        """
        if getattr(sys, "frozen", False):
            # Running as compiled .exe - use .exe location
            return Path(sys.executable).parent

        # Running as script - use project root (3 levels up from this file)
        return Path(__file__).parent.parent.parent

    def make_dirs(self) -> None:
        """Create all necessary application directories."""
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class Files:
    """Files for the application."""

    ICON_PATH = Directories.ICON_DIR / "icon.ico"
    SETTINGS_DB_PATH = Directories.SETTINGS_DIR / "settings.db"
    WALLPAPER_CACHE_PATH = Directories.CACHE_DIR / "wallpaper_cache.jpg"
    LOG_PATH = Directories.LOGS_DIR / "log.log"
    MEMORY_DB_PATH = ":memory:"


Directories().make_dirs()
