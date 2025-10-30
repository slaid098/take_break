"""Local wallpaper getter."""

from pathlib import Path
from random import choice

from loguru import logger

from src.constants.path import Directories

from .base import BaseWallpaperGetter


class LocalWallpaperGetter(BaseWallpaperGetter):
    """Local wallpaper getter."""

    def __init__(self, folder_path: Path | None = None) -> None:
        """Initialize the local wallpaper getter."""
        self.wallpaper_dir = folder_path or Directories.WALLPAPERS_DIR

    def get_wallpaper(self) -> Path | None:
        """Get a random wallpaper.

        Returns:
            Path to the wallpaper or None if failed.

        """
        if not self.wallpaper_dir.exists():
            logger.warning(f"Wallpapers directory {self.wallpaper_dir} does not exist")
            return None

        wallpapers = list(self.wallpaper_dir.glob("*.jpg")) + list(self.wallpaper_dir.glob("*.png"))

        if not wallpapers:
            logger.warning("No wallpapers found in the directory")
            return None

        return choice(wallpapers)
