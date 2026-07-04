"""Тесты сервиса настроек."""

from src.config.settings import Settings
from src.constants.settings import DEFAULT_WORK_DURATION_MIN, POMODORO_MODE_MIN, STANDARD_MODE_MIN
from src.db.db import Database


class TestSettings:
    """Тесты хранилища настроек."""

    def _make_settings(self) -> Settings:
        """Создать настройки с in-memory базой."""
        return Settings(db=Database(db_path=":memory:"))

    def test_get_focus_returns_empty_by_default(self) -> None:
        """get_focus возвращает пустую строку по умолчанию."""
        settings = self._make_settings()
        assert settings.get_focus() == ""

    def test_save_and_get_focus(self) -> None:
        """save_focus и get_focus работают корректно."""
        settings = self._make_settings()
        settings.save_focus("Изучать Go")
        assert settings.get_focus() == "Изучать Go"

    def test_is_first_run_true_by_default(self) -> None:
        """is_first_run возвращает True при первом запуске."""
        settings = self._make_settings()
        assert settings.is_first_run() is True

    def test_mark_first_run_complete(self) -> None:
        """mark_first_run_complete отключает is_first_run."""
        settings = self._make_settings()
        settings.mark_first_run_complete()
        assert settings.is_first_run() is False

    def test_set_invalid_work_duration_uses_default(self) -> None:
        """set_work_duration с некорректным значением использует default."""
        settings = self._make_settings()
        settings.set_work_duration(999)
        assert settings.get_work_duration() == DEFAULT_WORK_DURATION_MIN

    def test_set_valid_work_duration_pomodoro(self) -> None:
        """set_work_duration с 25 (Pomodoro) сохраняет."""
        settings = self._make_settings()
        settings.set_work_duration(POMODORO_MODE_MIN)
        assert settings.get_work_duration() == POMODORO_MODE_MIN

    def test_set_valid_work_duration_standard(self) -> None:
        """set_work_duration с 45 (Standard) сохраняет."""
        settings = self._make_settings()
        settings.set_work_duration(STANDARD_MODE_MIN)
        assert settings.get_work_duration() == STANDARD_MODE_MIN

    def test_online_wallpapers_default_true(self) -> None:
        """use_online_wallpapers по умолчанию True."""
        settings = self._make_settings()
        assert settings.get_use_online_wallpapers() is True

    def test_set_online_wallpapers_false(self) -> None:
        """set_use_online_wallpapers(False) сохраняет."""
        settings = self._make_settings()
        settings.set_use_online_wallpapers(False)
        assert settings.get_use_online_wallpapers() is False

    def test_move_timer_hotkey_default_empty(self) -> None:
        """get_move_timer_hotkey возвращает пустую строку по умолчанию."""
        settings = self._make_settings()
        assert settings.get_move_timer_hotkey() == ""

    def test_set_move_timer_hotkey(self) -> None:
        """set_move_timer_hotkey сохраняет хоткей."""
        settings = self._make_settings()
        settings.set_move_timer_hotkey("ctrl+alt+t")
        assert settings.get_move_timer_hotkey() == "ctrl+alt+t"

    def test_load_image_timeout_default(self) -> None:
        """get_load_image_timeout возвращает default."""
        settings = self._make_settings()
        assert settings.get_load_image_timeout() == 10
