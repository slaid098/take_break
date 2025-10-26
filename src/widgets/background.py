"""Background rendering utilities."""

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap


def paint_background(
    painter: QPainter,
    rect: QRect,
    wallpaper: QPixmap | None,
) -> None:
    """Paint background with wallpaper or solid color.

    Args:
        painter: The QPainter instance.
        rect: The rectangle to paint.
        wallpaper: The wallpaper to use, or None for solid background.

    """
    if wallpaper and not wallpaper.isNull():
        # Scale wallpaper to fit the screen while maintaining aspect ratio
        scaled_wallpaper = wallpaper.scaled(
            rect.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        # Center the image
        point = QPoint(
            (rect.width() - scaled_wallpaper.width()) // 2,
            (rect.height() - scaled_wallpaper.height()) // 2,
        )
        painter.drawPixmap(point, scaled_wallpaper)
        # Add a dark overlay for text readability
        painter.fillRect(rect, QColor(0, 0, 0, 10))
    else:
        # Fallback to a simple dark background
        painter.fillRect(rect, QColor(0, 0, 0, 220))
