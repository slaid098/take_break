"""Тесты директорий и путей приложения."""

from pathlib import Path

import pytest
from src.constants.path import Directories, Files, get_base_dir, get_bundle_dir


class TestDirectories:
    """Тесты директорий приложения."""

    def test_logo_dir_uses_logo_not_icon(self) -> None:
        """LOGO_DIR указывает на папку 'logo', а не 'icon'."""
        assert Directories.LOGO_DIR.name == "logo"

    def test_logo_path_points_to_logo_ico(self) -> None:
        """LOGO_PATH указывает на logo.ico."""
        assert Files.LOGO_PATH.name == "logo.ico"

    def test_logo_dir_uses_bundle_dir(self) -> None:
        """LOGO_DIR использует bundle dir (read-only ресурс)."""
        assert get_bundle_dir() in Directories.LOGO_DIR.parents

    def test_settings_dir_uses_base_dir(self) -> None:
        """SETTINGS_DIR использует base dir (user data)."""
        assert get_base_dir() in Directories.SETTINGS_DIR.parents

    def test_make_dirs_creates_user_directories(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """make_dirs создаёт все директории пользователя."""
        monkeypatch.setattr(Directories, "LOGS_DIR", tmp_path / "logs")
        monkeypatch.setattr(Directories, "CACHE_DIR", tmp_path / "cache")
        monkeypatch.setattr(Directories, "SETTINGS_DIR", tmp_path / "settings")
        monkeypatch.setattr(Directories, "LOGO_DIR", tmp_path / "logo")
        monkeypatch.setattr(Directories, "WALLPAPERS_DIR", tmp_path / "wallpapers")

        Directories().make_dirs()

        assert (tmp_path / "logs").is_dir()
        assert (tmp_path / "cache").is_dir()
        assert (tmp_path / "settings").is_dir()
        assert (tmp_path / "logo").is_dir()
        assert (tmp_path / "wallpapers").is_dir()

    def test_make_dirs_idempotent(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """make_dirs не падает при повторном вызове."""
        monkeypatch.setattr(Directories, "LOGS_DIR", tmp_path / "logs")
        monkeypatch.setattr(Directories, "CACHE_DIR", tmp_path / "cache")
        monkeypatch.setattr(Directories, "SETTINGS_DIR", tmp_path / "settings")
        monkeypatch.setattr(Directories, "LOGO_DIR", tmp_path / "logo")
        monkeypatch.setattr(Directories, "WALLPAPERS_DIR", tmp_path / "wallpapers")

        Directories().make_dirs()
        Directories().make_dirs()

    def test_memory_db_path_is_string(self) -> None:
        """MEMORY_DB_PATH — строка ':memory:'."""
        assert Files.MEMORY_DB_PATH == ":memory:"
