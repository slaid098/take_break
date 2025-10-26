"""Widget positioning service."""

from enum import StrEnum, auto

from PySide6.QtCore import QPoint


class WidgetPosition(StrEnum):
    """Timer widget position on screen."""

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_CENTER = auto()


def calculate_position(
    position: WidgetPosition,
    screen_width: int,
    screen_height: int,
    widget_width: int,
    widget_height: int,
) -> QPoint:
    """Calculate widget position based on screen geometry.

    Args:
        position: The desired position.
        screen_width: Screen width in pixels.
        screen_height: Screen height in pixels.
        widget_width: Widget width in pixels.
        widget_height: Widget height in pixels.

    Returns:
        The calculated QPoint position.

    """
    pos_name = position.lower()

    # Calculate Y position
    y = 0 if "top" in pos_name else screen_height - widget_height

    # Calculate X position
    if "left" in pos_name:
        x = 0
    elif "right" in pos_name:
        x = screen_width - widget_width
    else:  # center
        x = (screen_width - widget_width) // 2

    return QPoint(x, y)


def get_next_position(current: WidgetPosition) -> WidgetPosition:
    """Get the next position in cycle.

    Args:
        current: Current widget position.

    Returns:
        Next position in the cycle.

    """
    positions = list(WidgetPosition)
    current_index = positions.index(current)
    next_index = (current_index + 1) % len(positions)
    return positions[next_index]
