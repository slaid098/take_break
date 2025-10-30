"""Tests for config/texts.py."""

from src.config import texts
from src.constants.settings import DEFAULT_WORK_DURATION_MIN, POMODORO_MODE_MIN, STANDARD_MODE_MIN


def test_get_initial_text_without_previous_focus() -> None:
    """Test get_initial_text without previous focus and default work duration."""
    result = texts.Overlay.get_initial_text()

    # Should contain default duration
    assert f"{DEFAULT_WORK_DURATION_MIN}-минутный" in result
    # Should contain the emoji and basic instructions
    assert "⏱️" in result
    assert "Enter" in result


def test_get_initial_text_with_previous_focus() -> None:
    """Test get_initial_text with previous focus."""
    previous_focus = "Test focus text"
    result = texts.Overlay.get_initial_text(previous_focus)

    # Should contain previous focus text
    assert previous_focus in result
    # Should contain emoji and instructions
    assert "🎯" in result
    assert "Enter" in result


def test_get_initial_text_with_work_duration_25() -> None:
    """Test get_initial_text with 25 minute work duration."""
    result = texts.Overlay.get_initial_text(work_duration=POMODORO_MODE_MIN)

    assert f"{POMODORO_MODE_MIN}-минутный" in result


def test_get_initial_text_with_work_duration_45() -> None:
    """Test get_initial_text with 45 minute work duration."""
    result = texts.Overlay.get_initial_text(work_duration=STANDARD_MODE_MIN)

    assert f"{STANDARD_MODE_MIN}-минутный" in result


def test_get_initial_text_default_duration() -> None:
    """Test that passing None for work_duration uses default."""
    result = texts.Overlay.get_initial_text(work_duration=None)

    assert f"{DEFAULT_WORK_DURATION_MIN}-минутный" in result

