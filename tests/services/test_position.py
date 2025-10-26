"""Tests for position service."""

from PySide6.QtCore import QPoint

from src.services.position import WidgetPosition, calculate_position, get_next_position


def test_calculate_position_top_left() -> None:
    """Test calculating top-left position."""
    pos = calculate_position(
        WidgetPosition.TOP_LEFT,
        screen_width=1920,
        screen_height=1080,
        widget_width=200,
        widget_height=100,
    )

    assert pos == QPoint(0, 0)


def test_calculate_position_bottom_right() -> None:
    """Test calculating bottom-right position."""
    pos = calculate_position(
        WidgetPosition.BOTTOM_RIGHT,
        screen_width=1920,
        screen_height=1080,
        widget_width=200,
        widget_height=100,
    )

    assert pos == QPoint(1720, 980)


def test_calculate_position_center() -> None:
    """Test calculating center position."""
    pos = calculate_position(
        WidgetPosition.TOP_CENTER,
        screen_width=1920,
        screen_height=1080,
        widget_width=200,
        widget_height=100,
    )

    assert pos == QPoint(860, 0)


def test_get_next_position_cycles() -> None:
    """Test that position cycles through all 6 positions."""
    positions = list(WidgetPosition)
    current = WidgetPosition.TOP_LEFT

    for expected in positions:
        assert current == expected
        current = get_next_position(current)

    assert current == positions[0]
