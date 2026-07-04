"""Сервис позиционирования виджета."""

from enum import StrEnum, auto

from PySide6.QtCore import QPoint


class WidgetPosition(StrEnum):
    """Позиция виджета таймера на экране."""

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_CENTER = auto()


_POSITIONS = tuple(WidgetPosition)


def calculate_position(
    position: WidgetPosition,
    screen_width: int,
    screen_height: int,
    widget_width: int,
    widget_height: int,
) -> QPoint:
    """Вычислить позицию виджета на основе геометрии экрана.

    Args:
        position: Желаемая позиция.
        screen_width: Ширина экрана в пикселях.
        screen_height: Высота экрана в пикселях.
        widget_width: Ширина виджета в пикселях.
        widget_height: Высота виджета в пикселях.

    Returns:
        Вычисленная позиция QPoint.

    """
    pos_name = position.lower()

    y = 0 if "top" in pos_name else screen_height - widget_height

    if "left" in pos_name:
        x = 0
    elif "right" in pos_name:
        x = screen_width - widget_width
    else:
        x = (screen_width - widget_width) // 2

    return QPoint(x, y)


def get_next_position(current: WidgetPosition) -> WidgetPosition:
    """Получить следующую позицию в цикле.

    Args:
        current: Текущая позиция виджета.

    Returns:
        Следующая позиция в цикле.

    """
    current_index = _POSITIONS.index(current)
    next_index = (current_index + 1) % len(_POSITIONS)
    return _POSITIONS[next_index]
