"""Wallpaper management service."""

import threading
from pathlib import Path

from PySide6.QtGui import QPixmap

from .getter.local import LocalWallpaperGetter
from .getter.picsum import PicsumWallpaperGetter


class WallpaperManager:
    """Manages wallpaper loading and selection."""

    def __init__(
        self,
        width: int,
        height: int,
        use_online: bool = True,
        cache_file_path: Path | None = None,
        local_folder_path: Path | None = None,
    ) -> None:
        """Initialize the wallpaper manager.

        Args:
            width: Screen width.
            height: Screen height.
            use_online: Whether to use online wallpapers.
            cache_file_path: Path to the cache file.
            local_folder_path: Path to the local folder.

        """
        self._use_online = use_online
        self._local_getter = LocalWallpaperGetter(local_folder_path)
        self._picsum_getter = PicsumWallpaperGetter(width, height, cache_file_path)
        self._wallpaper = self._set_initial_wallpaper()
        self._fetch_wallpaper()

    def get_wallpaper(self) -> QPixmap | None:
        """Get a random wallpaper.

        Returns:
            QPixmap with the wallpaper or None if failed.

        """
        self._fetch_wallpaper()
        return self._wallpaper

    def _fetch_wallpaper(self) -> None:
        """Fetch a wallpaper."""

        def _fetch() -> None:
            if self._use_online:
                path = self._picsum_getter.get_wallpaper()
            else:
                path = self._local_getter.get_wallpaper()

            if path:
                self._wallpaper = QPixmap(str(path))
            else:
                self._wallpaper = None

        threading.Thread(daemon=True, target=_fetch).start()

    def set_use_online(self, use_online: bool) -> None:
        """Set whether to use online wallpapers."""
        self._use_online = use_online

    def _set_initial_wallpaper(self) -> QPixmap | None:
        """Set initial wallpaper from cache or local files."""
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
