"""Получение обоев с Picsum."""

from pathlib import Path

import requests
from loguru import logger

from src.constants.path import Files
from src.constants.settings import LOAD_IMAGE_TIMEOUT_DEFAULT
from src.constants.url import PICSUM_URL

from .base import BaseWallpaperGetter


class PicsumWallpaperGetter(BaseWallpaperGetter):
    """Получение случайных обоев с picsum.photos."""

    def __init__(self, width: int, height: int, cache_file_path: Path | None = None) -> None:
        """Инициализировать getter обоев с Picsum.

        Args:
            width: Ширина изображения.
            height: Высота изображения.
            cache_file_path: Путь к файлу кэша.

        """
        self.timeout = LOAD_IMAGE_TIMEOUT_DEFAULT
        self.width = width
        self.height = height
        self.cache_path = cache_file_path or Files.WALLPAPER_CACHE_PATH

    def get_wallpaper(self) -> Path | None:
        """Получить случайные обои с Picsum.

        Returns:
            Путь к скачанному изображению или None при ошибке.

        """
        url = PICSUM_URL.format(width=self.width, height=self.height)
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_bytes(response.content)
        except requests.RequestException as e:
            logger.warning(f"Не удалось загрузить обои с {url}: {e}")
            return None
        else:
            logger.debug(f"Онлайн-обои с {url} сохранены")
            return self.cache_path
