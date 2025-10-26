"""Tests for App orchestrator."""

from pytestqt.qtbot import QtBot

from src.services.position import WidgetPosition, calculate_position
from src.widgets.timer import TimerWidget


def test_timer_widget_positions_correctly(qtbot: QtBot) -> None:
    """Test that timer widget positions correctly for all widget positions."""
    widget = TimerWidget()
    qtbot.addWidget(widget)

    # Simulate all 6 positions
    screen_width = 1920

    # Simulate availableGeometry (accounting for taskbar)
    available_height = 1040  # Example: 40px taskbar

    for position in WidgetPosition:
        pos = calculate_position(
            position, screen_width, available_height, widget.width(), widget.height(),
        )

        # Check position is within available screen bounds
        assert 0 <= pos.x() <= screen_width
        assert 0 <= pos.y() <= available_height

