"""Тесты сервиса автозапуска."""

from unittest.mock import patch

from src.services import autostart


class TestAutostart:
    """Тесты управления автозапуском в Windows."""

    def test_get_exe_path_returns_none_when_not_frozen(self) -> None:
        """get_exe_path возвращает None для Python-скрипта."""
        with patch("sys.frozen", False, create=True):
            assert autostart.get_exe_path() is None

    def test_is_autostart_enabled_returns_false_on_non_windows(self) -> None:
        """is_autostart_enabled возвращает False на non-Windows."""
        with patch.object(autostart, "winreg", None):
            assert autostart.is_autostart_enabled() is False

    def test_enable_autostart_noop_on_non_windows(self) -> None:
        """enable_autostart no-op на non-Windows."""
        with patch.object(autostart, "winreg", None):
            autostart.enable_autostart()

    def test_disable_autostart_noop_on_non_windows(self) -> None:
        """disable_autostart no-op на non-Windows."""
        with patch.object(autostart, "winreg", None):
            autostart.disable_autostart()

    def test_enable_autostart_noop_when_not_frozen(self) -> None:
        """enable_autostart no-op для Python-скрипта."""
        with patch("sys.frozen", False, create=True):
            autostart.enable_autostart()
