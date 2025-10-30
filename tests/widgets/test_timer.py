"""Tests for timer widget."""

from datetime import timedelta

from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from src.constants.settings import MAX_FOCUS_LENGTH, RED_SECOND_THRESHOLD
from src.widgets.styles import TIMER_TIME_RED_STYLE
from src.widgets.timer import TimerWidget


def test_set_focus_text_shows_label(qtbot: QtBot) -> None:
    """Test that focus label is shown when text is set."""
    widget = TimerWidget()
    qtbot.addWidget(widget)

    widget.set_focus_text("test focus")

    assert widget.focus_label.text() == "🎯 test focus"
    assert not widget.focus_label.isHidden()


def test_set_focus_text_hides_when_empty(qtbot: QtBot) -> None:
    """Test that focus label is hidden when text is empty."""
    widget = TimerWidget()
    qtbot.addWidget(widget)
    widget.set_focus_text("initial")

    widget.set_focus_text("")

    assert not widget.focus_label.isVisible()


def test_update_time_turns_red_under_threshold(qtbot: QtBot) -> None:
    """Test that timer turns red when remaining time is under threshold."""
    widget = TimerWidget()
    qtbot.addWidget(widget)

    widget.update_time(timedelta(seconds=RED_SECOND_THRESHOLD - 1))

    assert TIMER_TIME_RED_STYLE in widget.time_label.styleSheet()


def test_timer_has_fixed_width(qtbot: QtBot) -> None:
    """Test that timer has fixed width based on MAX_FOCUS_LENGTH."""
    widget = TimerWidget()
    qtbot.addWidget(widget)

    initial_width = widget.width()

    # Width should remain constant
    widget.set_focus_text("test")
    widget.set_focus_text("a very long focus text that should not change width")
    widget.set_focus_text("")

    assert widget.width() == initial_width
    assert widget.width() > 0


def test_focus_text_within_widget_bounds(qtbot: QtBot) -> None:
    """Test that focus text is within widget bounds."""
    widget = TimerWidget()
    qtbot.addWidget(widget)
    widget.show()

    widget.set_focus_text("Только Флеред")

    # Focus label should be visible and within widget geometry
    assert widget.focus_label.isVisible()
    assert widget.focus_label.geometry().bottom() <= widget.height()


def test_timer_has_translucent_background(qtbot: QtBot) -> None:
    """Test that timer widget has translucent background for custom painting."""
    widget = TimerWidget()
    qtbot.addWidget(widget)

    assert widget.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


def test_timer_size_based_on_max_focus_length(qtbot: QtBot) -> None:
    """Test that timer size accommodates MAX_FOCUS_LENGTH."""
    widget = TimerWidget()
    qtbot.addWidget(widget)
    widget.show()

    # Set focus with MAX_FOCUS_LENGTH characters
    max_focus = "A" * MAX_FOCUS_LENGTH
    widget.set_focus_text(max_focus)

    # Focus label should be fully visible within widget bounds
    assert widget.focus_label.isVisible()
    focus_geometry = widget.focus_label.geometry()
    assert focus_geometry.right() <= widget.width()
    assert focus_geometry.bottom() <= widget.height()

