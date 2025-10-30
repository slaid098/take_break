"""Picsum wallpaper getter."""

from pathlib import Path

import requests
from loguru import logger

from src.constants.path import Files
from src.constants.settings import LOAD_IMAGE_TIMEOUT_DEFAULT
from src.constants.url import PICSUM_URL

from .base import BaseWallpaperGetter


class PicsumWallpaperGetter(BaseWallpaperGetter):
    """Picsum wallpaper getter."""

    def __init__(self, width: int, height: int, cache_file_path: Path | None = None) -> None:
        """Initialize the Picsum wallpaper getter."""
        self.timeout = LOAD_IMAGE_TIMEOUT_DEFAULT
        self.width = width
        self.height = height
        self.cache_path = cache_file_path or Files.WALLPAPER_CACHE_PATH

    def get_wallpaper(self) -> Path | None:
        """Get a random wallpaper.

        Returns:
            Path to the wallpaper or None if failed.

        """
        url = PICSUM_URL.format(width=self.width, height=self.height)
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            self.cache_path.write_bytes(response.content)
            logger.debug(f"online image from {url} saved succefully")
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch online wallpaper from {url}: {e}")
            return None
        else:
            return self.cache_path
