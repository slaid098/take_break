"""Base class for getting wallpapers."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseWallpaperGetter(ABC):
    """Base class for getting wallpapers."""

    @abstractmethod
    def get_wallpaper(self) -> Path | None:
        """Get a random wallpaper."""
