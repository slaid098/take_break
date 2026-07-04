"""Управление обоями для overlay."""

import threading
from pathlib import Path

from PySide6.QtGui import QPixmap

from .getter.local import LocalWallpaperGetter
from .getter.picsum import PicsumWallpaperGetter


class WallpaperManager:
    """Управляет загрузкой и выбором обоев."""

    def __init__(
        self,
        width: int,
        height: int,
        use_online: bool = True,
        cache_file_path: Path | None = None,
        local_folder_path: Path | None = None,
    ) -> None:
        """Инициализировать менеджер обоев.

        Args:
            width: Ширина экрана.
            height: Высота экрана.
            use_online: Использовать ли онлайн-обои.
            cache_file_path: Путь к файлу кэша.
            local_folder_path: Путь к локальной папке с обоями.

        """
        self._use_online = use_online
        self._local_getter = LocalWallpaperGetter(local_folder_path)
        self._picsum_getter = PicsumWallpaperGetter(width, height, cache_file_path)
        self._lock = threading.Lock()
        self._wallpaper: QPixmap | None = self._set_initial_wallpaper()
        self._fetch_wallpaper()

    def get_wallpaper(self) -> QPixmap | None:
        """Получить текущие обои.

        Returns:
            QPixmap с обоями или None если не удалось загрузить.

        """
        self._fetch_wallpaper()
        with self._lock:
            return self._wallpaper

    def _fetch_wallpaper(self) -> None:
        """Загрузить обои в фоновом потоке."""

        def _fetch() -> None:
            if self._use_online:
                path = self._picsum_getter.get_wallpaper()
            else:
                path = self._local_getter.get_wallpaper()

            pixmap = QPixmap(str(path)) if path else None

            with self._lock:
                self._wallpaper = pixmap

        threading.Thread(daemon=True, target=_fetch).start()

    def set_use_online(self, use_online: bool) -> None:
        """Установить режим загрузки обоев.

        Args:
            use_online: True для онлайн-обоев, False для локальных.

        """
        self._use_online = use_online

    def _set_initial_wallpaper(self) -> QPixmap | None:
        """Установить начальные обои из кэша или локальных файлов."""
        wallpaper: QPixmap | None = None

        if self._use_online and self._picsum_getter.cache_path.exists():
            wallpaper = QPixmap(str(self._picsum_getter.cache_path))
            if wallpaper.isNull():
                wallpaper = None

        if not wallpaper:
            local_path = self._local_getter.get_wallpaper()
            if local_path:
                wallpaper = QPixmap(str(local_path))
                if wallpaper.isNull():
                    wallpaper = None

        return wallpaper
