"""Tests for settings storage service."""

import json
from pathlib import Path

from src.config import settings
from src.services.settings_storage import SettingsStorage


def test_save_and_get_focus(temp_settings_dir: Path) -> None:
    """Test saving and loading focus text."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    storage.save_focus("test focus")
    focus = storage.get_focus()

    assert focus == "test focus"


def test_first_run_lifecycle(temp_settings_dir: Path) -> None:
    """Test first run flag lifecycle."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    assert storage.is_first_run()

    storage.mark_first_run_complete()

    assert not storage.is_first_run()


def test_creates_directory_if_missing(temp_settings_dir: Path) -> None:
    """Test that storage creates directory if it doesn't exist."""
    SettingsStorage(settings_dir=temp_settings_dir)

    assert temp_settings_dir.exists()


def test_empty_focus_by_default(temp_settings_dir: Path) -> None:
    """Test that empty focus is returned by default."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    focus = storage.get_focus()

    assert focus == ""


def test_json_format(temp_settings_dir: Path) -> None:
    """Test that settings are saved in correct JSON format."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)
    storage.save_focus("test")

    with (temp_settings_dir / "settings.json").open() as f:
        data = json.load(f)

    assert data == {
        "focus": "test",
        "first_run_complete": False,
        "use_online_wallpapers": True,
        "work_duration": settings.DEFAULT_WORK_DURATION_MIN,
    }


def test_focus_persists_on_empty_save(temp_settings_dir: Path) -> None:
    """Test that empty focus is saved correctly (not ignored)."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    # Save initial focus
    storage.save_focus("Previous focus")
    loaded = storage.get_focus()
    assert loaded == "Previous focus"

    # Save empty focus
    storage.save_focus("")

    # Empty string should be saved (not ignored)
    loaded_empty = storage.get_focus()
    assert loaded_empty == ""

    # Verify JSON contains empty string
    with (temp_settings_dir / "settings.json").open() as f:
        data = json.load(f)

    assert data == {
        "focus": "",
        "first_run_complete": False,
        "use_online_wallpapers": True,
        "work_duration": settings.DEFAULT_WORK_DURATION_MIN,
    }


def test_get_work_duration(temp_settings_dir: Path) -> None:
    """Test getting work duration setting."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    # Default should be 45
    duration = storage.get_work_duration()
    assert duration == settings.DEFAULT_WORK_DURATION_MIN


def test_set_work_duration(temp_settings_dir: Path) -> None:
    """Test setting work duration."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    # Set to 25 minutes
    storage.set_work_duration(settings.POMODORO_MODE_MIN)
    assert storage.get_work_duration() == settings.POMODORO_MODE_MIN

    # Set to 45 minutes
    storage.set_work_duration(settings.STANDARD_MODE_MIN)
    assert storage.get_work_duration() == settings.STANDARD_MODE_MIN

    # Invalid duration should use default
    storage.set_work_duration(100)
    assert storage.get_work_duration() == settings.DEFAULT_WORK_DURATION_MIN


def test_get_move_timer_hotkey(temp_settings_dir: Path) -> None:
    """Test getting move timer hotkey."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    # Default should be empty (not set)
    hotkey = storage.get_move_timer_hotkey()
    assert hotkey == ""


def test_set_move_timer_hotkey(temp_settings_dir: Path) -> None:
    """Test setting move timer hotkey."""
    storage = SettingsStorage(settings_dir=temp_settings_dir)

    # Set and verify hotkey
    test_hotkey = "ctrl+alt+t"
    storage.set_move_timer_hotkey(test_hotkey)
    assert storage.get_move_timer_hotkey() == test_hotkey


def test_move_timer_hotkey_persistence(temp_settings_dir: Path) -> None:
    """Test that move timer hotkey persists across storage instances."""
    # Create first instance and set hotkey
    storage1 = SettingsStorage(settings_dir=temp_settings_dir)
    test_hotkey = "ctrl+shift+m"
    storage1.set_move_timer_hotkey(test_hotkey)

    # Create second instance with same directory
    storage2 = SettingsStorage(settings_dir=temp_settings_dir)

    # Verify hotkey is loaded correctly
    assert storage2.get_move_timer_hotkey() == test_hotkey

