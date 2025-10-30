"""Tests for settings storage service."""


from src.config.settings import Settings
from src.constants.settings import DEFAULT_WORK_DURATION_MIN, POMODORO_MODE_MIN, STANDARD_MODE_MIN


def test_save_and_get_focus(test_settings: Settings) -> None:
    """Test saving and loading focus text."""
    test_settings.save_focus("test focus")
    focus = test_settings.get_focus()

    assert focus == "test focus"


def test_first_run_lifecycle(test_settings: Settings) -> None:
    """Test first run flag lifecycle."""
    assert test_settings.is_first_run()

    test_settings.mark_first_run_complete()

    assert not test_settings.is_first_run()


def test_empty_focus_by_default(test_settings: Settings) -> None:
    """Test that empty focus is returned by default."""
    focus = test_settings.get_focus()

    assert focus == ""


def test_json_format(test_settings: Settings) -> None:
    """Test that settings are saved in correct SQLite format."""
    test_settings.save_focus("test")

    # Settings are now stored in SQLite, not JSON
    assert test_settings.get_focus() == "test"


def test_focus_persists_on_empty_save(test_settings: Settings) -> None:
    """Test that empty focus is saved correctly (not ignored)."""
    # Save initial focus
    test_settings.save_focus("Previous focus")
    loaded = test_settings.get_focus()
    assert loaded == "Previous focus"

    # Save empty focus
    test_settings.save_focus("")

    # Empty string should be saved (not ignored)
    loaded_empty = test_settings.get_focus()
    assert loaded_empty == ""

    # Verify SQLite contains empty string
    assert test_settings.get_focus() == ""


def test_get_work_duration(test_settings: Settings) -> None:
    """Test getting work duration setting."""
    # Default should be 45
    duration = test_settings.get_work_duration()
    assert duration == DEFAULT_WORK_DURATION_MIN


def test_set_work_duration(test_settings: Settings) -> None:
    """Test setting work duration."""
    # Set to 25 minutes
    test_settings.set_work_duration(POMODORO_MODE_MIN)
    assert test_settings.get_work_duration() == POMODORO_MODE_MIN

    # Set to 45 minutes
    test_settings.set_work_duration(STANDARD_MODE_MIN)
    assert test_settings.get_work_duration() == STANDARD_MODE_MIN

    # Invalid duration should use default
    test_settings.set_work_duration(100)
    assert test_settings.get_work_duration() == DEFAULT_WORK_DURATION_MIN


def test_get_move_timer_hotkey(test_settings: Settings) -> None:
    """Test getting move timer hotkey."""
    # Default should be empty (not set)
    hotkey = test_settings.get_move_timer_hotkey()
    assert hotkey == ""


def test_set_move_timer_hotkey(test_settings: Settings) -> None:
    """Test setting move timer hotkey."""
    # Set and verify hotkey
    test_hotkey = "ctrl+alt+t"
    test_settings.set_move_timer_hotkey(test_hotkey)
    assert test_settings.get_move_timer_hotkey() == test_hotkey


def test_move_timer_hotkey_persistence(test_settings: Settings) -> None:
    """Test that move timer hotkey persists across storage instances."""
    # Create first instance and set hotkey
    test_hotkey = "ctrl+shift+m"
    test_settings.set_move_timer_hotkey(test_hotkey)

    # Verify hotkey is loaded correctly
    assert test_settings.get_move_timer_hotkey() == test_hotkey

