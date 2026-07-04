"""Локальный getter обоев."""

from pathlib import Path
from random import choice

from loguru import logger

from src.constants.path import Directories

from .base import BaseWallpaperGetter


class LocalWallpaperGetter(BaseWallpaperGetter):
    """Получение случайных обоев из локальной папки."""

    def __init__(self, folder_path: Path | None = None) -> None:
        """Инициализировать локальный getter обоев.

        Args:
            folder_path: Путь к папке с обоями.

        """
        self.wallpaper_dir = folder_path or Directories.WALLPAPERS_DIR

    def get_wallpaper(self) -> Path | None:
        """Получить случайные обои из локальной папки.

        Returns:
            Путь к изображению или None если не найдено.

        """
        if not self.wallpaper_dir.exists():
            logger.warning(f"Папка обоев {self.wallpaper_dir} не существует")
            return None

        wallpapers = list(self.wallpaper_dir.glob("*.jpg")) + list(self.wallpaper_dir.glob("*.png"))

        if not wallpapers:
            logger.warning("В папке не найдено обоев")
            return None

        return choice(wallpapers)
