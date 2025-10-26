"""Wallpaper management service."""

import random
from collections.abc import Callable
from pathlib import Path
from threading import Lock

import requests
from loguru import logger
from PySide6.QtCore import QByteArray, QRunnable, QThreadPool
from PySide6.QtGui import QPixmap

from src.config import settings


class WallpaperLoadTask(QRunnable):
    """Background task for loading wallpapers."""

    def __init__(
        self,
        url: str,
        callback: Callable[[QPixmap | None], None],
        save_to_cache: bool = False,
    ) -> None:
        """Initialize the wallpaper load task.

        Args:
            url: URL to fetch wallpaper from.
            callback: Function to call with the loaded QPixmap or None.
            save_to_cache: Whether to save loaded wallpaper to cache.

        """
        super().__init__()
        self.url = url
        self.callback = callback
        self.save_to_cache = save_to_cache

    def run(self) -> None:
        """Execute the wallpaper loading task."""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(response.content))

            if not pixmap.isNull():
                logger.debug("Online wallpaper loaded successfully")

                # Save to cache if needed
                if self.save_to_cache:
                    pixmap.save(str(settings.WALLPAPER_CACHE_PATH), "JPG")
                    logger.debug("Saved wallpaper to cache")

                self.callback(pixmap)
            else:
                logger.warning("Failed to load online wallpaper: invalid image data")
                self.callback(None)

        except requests.RequestException as e:
            logger.warning(f"Failed to load online wallpaper: {e}")
            self.callback(None)


class WallpaperManager:
    """Manages wallpaper loading and selection."""

    PICSUM_URL = "https://picsum.photos/{width}/{height}"

    def __init__(self, wallpapers_dir: Path | None = None, use_online: bool = False) -> None:
        """Initialize the wallpaper manager.

        Args:
            wallpapers_dir: Directory containing wallpapers. Defaults to settings.WALLPAPERS_DIR.
            use_online: Whether to use online wallpapers.

        """
        self.use_online = use_online
        self.wallpapers_dir = wallpapers_dir or settings.WALLPAPERS_DIR
        self._wallpapers: list[Path] = self._load_wallpapers()

        # Dimensions for preloading
        self._preload_width = settings.PRELOAD_WIDTH_DEFAULT
        self._preload_height = settings.PRELOAD_HEIGHT_DEFAULT
        self._thread_pool = QThreadPool()
        self._preload_lock = Lock()

    def _load_wallpapers(self) -> list[Path]:
        """Load wallpapers from the app_data directory.

        Returns:
            A list of paths to the wallpaper files.

        """
        return list(self.wallpapers_dir.glob("*.jpg")) + list(
            self.wallpapers_dir.glob("*.png"),
        )

    def _fetch_online_wallpaper(self, width: int, height: int) -> QPixmap | None:
        """Fetch wallpaper from Lorem Picsum (synchronous, blocks UI).

        Args:
            width: Screen width.
            height: Screen height.

        Returns:
            QPixmap with online wallpaper or None on failure.

        """
        try:
            url = self.PICSUM_URL.format(width=width, height=height)
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(response.content))

            if not pixmap.isNull():
                logger.debug("Online wallpaper loaded successfully")
                return pixmap
            logger.warning("Failed to load online wallpaper: invalid image data")
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch online wallpaper: {e}")
        else:
            return None

    def _load_from_cache(self) -> QPixmap | None:
        """Load wallpaper from disk cache.

        Returns:
            QPixmap with cached wallpaper or None if not available.

        """
        if not settings.WALLPAPER_CACHE_PATH.exists():
            return None

        try:
            pixmap = QPixmap(str(settings.WALLPAPER_CACHE_PATH))
            if not pixmap.isNull():
                logger.debug("Loaded wallpaper from cache")
                return pixmap
        except Exception as e:
            logger.warning(f"Failed to load wallpaper from cache: {e}")
            return None
        else:
            return None

    def _save_to_cache(self, pixmap: QPixmap) -> None:
        """Save wallpaper to disk cache.

        Args:
            pixmap: The pixmap to save.

        """
        try:
            pixmap.save(str(settings.WALLPAPER_CACHE_PATH), "JPG")
            logger.debug("Saved wallpaper to cache")
        except Exception as e:
            logger.warning(f"Failed to save wallpaper to cache: {e}")

    def _preload_next_wallpaper(self) -> None:
        """Preload next wallpaper in background thread and save to cache."""
        if not self.use_online:
            return

        url = self.PICSUM_URL.format(width=self._preload_width, height=self._preload_height)

        def on_preload_complete(pixmap: QPixmap | None) -> None:
            """Handle preload completion.

            Args:
                pixmap: The loaded pixmap or None if failed.

            """
            if pixmap and not pixmap.isNull():
                self._save_to_cache(pixmap)
                logger.debug("Wallpaper preloaded and saved to cache")

        task = WallpaperLoadTask(url, on_preload_complete, save_to_cache=True)
        self._thread_pool.start(task)

    def start_preloading(self, width: int, height: int) -> None:
        """Start preloading wallpaper for future use.

        Loads from cache if available, otherwise loads from internet.

        Args:
            width: Screen width.
            height: Screen height.

        """
        self._preload_width = width
        self._preload_height = height

        if not self.use_online:
            return

        # Check if cache exists
        if settings.WALLPAPER_CACHE_PATH.exists():
            logger.debug("Wallpaper cache exists, will use cached version")
            return

        # No cache, load from internet and save
        logger.debug(f"Loading wallpaper for {width}x{height} and saving to cache")
        online_pixmap = self._fetch_online_wallpaper(width, height)
        if online_pixmap:
            self._save_to_cache(online_pixmap)

    def get_random_wallpaper(self) -> QPixmap | None:
        """Get a random wallpaper.

        Loads from cache instantly and triggers background update of cache.

        Returns:
            A random wallpaper as QPixmap, or None if no wallpapers available.

        """
        # Try online first if enabled
        if self.use_online:
            # Load from cache (instant)
            cached_pixmap = self._load_from_cache()
            if cached_pixmap:
                logger.debug("Returning wallpaper from cache")

                # Start loading next wallpaper in background
                with self._preload_lock:
                    self._preload_next_wallpaper()

                return cached_pixmap

            # No cache, fallback to sync loading
            logger.debug("No cache available, falling back to synchronous load")
            online_pixmap = self._fetch_online_wallpaper(self._preload_width, self._preload_height)
            if online_pixmap:
                self._save_to_cache(online_pixmap)
                # Start preloading next one
                self._preload_next_wallpaper()
                return online_pixmap

            logger.info("Falling back to local wallpapers")

        # Fallback to local wallpapers
        if not self._wallpapers:
            logger.warning("No local wallpapers available")
            return None

        wallpaper_path = random.choice(self._wallpapers)
        return QPixmap(str(wallpaper_path))

    def set_use_online(self, enabled: bool) -> None:
        """Set whether to use online wallpapers.

        Args:
            enabled: Whether to enable online wallpapers.

        """
        self.use_online = enabled

        # If enabling online wallpapers and we have dimensions, start preloading
        if enabled:
            self.start_preloading(self._preload_width, self._preload_height)
