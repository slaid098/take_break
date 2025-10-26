"""Tests for overlay widget."""

from datetime import UTC, datetime

from PySide6.QtGui import QCloseEvent
from pytestqt.qtbot import QtBot

from src.config import settings
from src.widgets.overlay import BlockingOverlay


def test_overlay_blocks_close_when_blocking(qtbot: QtBot) -> None:
    """Test that overlay blocks close event when blocking mode is active."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Set blocking mode
    overlay.is_blocking = True

    # Try to close
    event = QCloseEvent()
    overlay.closeEvent(event)

    # Event should be ignored
    assert not event.isAccepted()


def test_overlay_emits_close_signal_when_not_blocking(qtbot: QtBot) -> None:
    """Test that overlay emits close signal when blocking mode is not active."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Set non-blocking mode
    overlay.is_blocking = False

    # Monitor signal
    with qtbot.waitSignal(overlay.close_requested, timeout=1000):
        event = QCloseEvent()
        overlay.closeEvent(event)

    # Event should be accepted
    assert event.isAccepted()


def test_overlay_default_is_not_blocking() -> None:
    """Test that overlay defaults to non-blocking mode."""
    overlay = BlockingOverlay()

    assert overlay.is_blocking is False


def test_overlay_hide_focus_input(qtbot: QtBot) -> None:
    """Test hiding focus input field."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    overlay.hide_focus_input()

    assert not overlay.focus_input.isVisible()


def test_overlay_show_focus_input(qtbot: QtBot) -> None:
    """Test showing focus input field."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Show widget to make visibility checks work
    overlay.show()

    overlay.focus_input.hide()
    overlay.show_focus_input()

    assert overlay.focus_input.isVisible()


def test_overlay_hide_extra_rest_timer(qtbot: QtBot) -> None:
    """Test hiding extra rest timer."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)


    overlay.show_extra_rest_timer(datetime.now(UTC))
    overlay.hide_extra_rest_timer()

    assert not overlay.extra_rest_label.isVisible()
    assert not overlay.extra_rest_timer.isActive()
    assert overlay.extra_rest_start is None


def test_overlay_focus_input_has_fixed_width(qtbot: QtBot) -> None:
    """Test that focus input has a calculated fixed width."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Focus input should have a fixed width greater than 0
    assert overlay.focus_input.width() > 0


def test_overlay_focus_input_has_reasonable_width(qtbot: QtBot) -> None:
    """Test that focus input has reasonable width boundaries."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Width should be within reasonable bounds
    # Minimum: at least 300px to show some text
    # Maximum: not more than 2000px even with large MAX_FOCUS_LENGTH
    min_width = 300
    max_width = 2000
    width = overlay.focus_input.width()
    assert min_width <= width <= max_width


def test_overlay_focus_input_accepts_max_length_text(qtbot: QtBot) -> None:
    """Test that focus input can accept MAX_FOCUS_LENGTH characters."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    # Create text of maximum length
    max_text = "A" * settings.MAX_FOCUS_LENGTH

    # Set text and verify it was accepted
    overlay.focus_input.setText(max_text)
    assert overlay.focus_input.text() == max_text

    # Try to add one more character - should be rejected
    overlay.focus_input.setText(max_text + "B")
    assert overlay.focus_input.text() == max_text


def test_overlay_focus_input_respects_max_length(qtbot: QtBot) -> None:
    """Test that focus input respects MAX_FOCUS_LENGTH setting."""
    overlay = BlockingOverlay()
    qtbot.addWidget(overlay)

    assert overlay.focus_input.maxLength() == settings.MAX_FOCUS_LENGTH

