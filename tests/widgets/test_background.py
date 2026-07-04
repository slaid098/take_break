"""Тесты рендеринга фона."""

from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QImage, QPainter, QPixmap
from src.widgets.background import paint_background


class TestPaintBackground:
    """Тесты функции paint_background."""

    def test_paint_with_wallpaper(self, qapp: None) -> None:
        """paint_background рисует обои если переданы."""
        image = QImage(100, 100, QImage.Format.Format_ARGB32)
        painter = QPainter(image)

        wallpaper = QPixmap(50, 50)
        wallpaper.fill(QColor("blue"))

        paint_background(painter, QRect(0, 0, 100, 100), wallpaper)

        painter.end()
        assert not image.isNull()

    def test_paint_without_wallpaper(self, qapp: None) -> None:
        """paint_background рисует тёмный фон без обоев."""
        image = QImage(100, 100, QImage.Format.Format_ARGB32)
        painter = QPainter(image)

        paint_background(painter, QRect(0, 0, 100, 100), None)

        painter.end()
        assert not image.isNull()

    def test_paint_with_null_wallpaper(self, qapp: None) -> None:
        """paint_background рисует тёмный фон для null pixmap."""
        image = QImage(100, 100, QImage.Format.Format_ARGB32)
        painter = QPainter(image)

        wallpaper = QPixmap()
        assert wallpaper.isNull()

        paint_background(painter, QRect(0, 0, 100, 100), wallpaper)

        painter.end()
        assert not image.isNull()
