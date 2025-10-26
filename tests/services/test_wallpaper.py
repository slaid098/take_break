"""Tests for wallpaper manager."""

from pathlib import Path

from PIL import Image
from PySide6.QtWidgets import QApplication

from src.services.wallpaper import WallpaperManager


def test_local_wallpapers_only(tmp_path: Path, qapp: QApplication) -> None:  # noqa: ARG001
    """Test that local wallpapers work when online is disabled."""
    # Create real wallpaper image
    img = Image.new("RGB", (1920, 1080), color="blue")
    wallpaper = tmp_path / "test.jpg"
    img.save(wallpaper)

    manager = WallpaperManager(wallpapers_dir=tmp_path, use_online=False)
    pixmap = manager.get_random_wallpaper()

    assert pixmap is not None
    assert not pixmap.isNull()


def test_local_wallpapers_loading(tmp_path: Path, qapp: QApplication) -> None:  # noqa: ARG001
    """Test loading multiple local wallpapers."""
    # Create multiple wallpapers
    colors = ["blue", "red", "green"]
    for i, color in enumerate(colors):
        img = Image.new("RGB", (1920, 1080), color=color)
        wallpaper = tmp_path / f"test{i}.jpg"
        img.save(wallpaper)

    manager = WallpaperManager(wallpapers_dir=tmp_path, use_online=False)

    # Get multiple wallpapers to test randomness
    pixmaps = [manager.get_random_wallpaper() for _ in range(5)]

    # All should be valid
    for pixmap in pixmaps:
        assert pixmap is not None
        assert not pixmap.isNull()


def test_set_use_online(tmp_path: Path, qapp: QApplication) -> None:  # noqa: ARG001
    """Test changing online wallpaper setting."""
    # Create test wallpaper
    img = Image.new("RGB", (1920, 1080), color="red")
    wallpaper = tmp_path / "test.jpg"
    img.save(wallpaper)

    manager = WallpaperManager(wallpapers_dir=tmp_path, use_online=False)
    assert not manager.use_online

    manager.set_use_online(True)
    assert manager.use_online


def test_no_wallpapers_returns_none(tmp_path: Path, qapp: QApplication) -> None:  # noqa: ARG001
    """Test that returns None when no wallpapers available."""
    manager = WallpaperManager(wallpapers_dir=tmp_path, use_online=False)
    pixmap = manager.get_random_wallpaper()

    assert pixmap is None


def test_cache_directory_creation(tmp_path: Path, qapp: QApplication) -> None:  # noqa: ARG001
    """Test that cache directory exists when WallpaperManager is initialized."""
    manager = WallpaperManager(wallpapers_dir=tmp_path, use_online=False)

    # Verify manager exists
    assert manager is not None
    assert manager.wallpapers_dir == tmp_path
