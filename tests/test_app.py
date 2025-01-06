"""Тесты для основного модуля приложения."""

import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from PyQt6.QtCore import QPoint, QSize, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# Добавляем путь к пакету в PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from take_break.app import TakeBreakApp


# Создаем базовый класс для виджетов
class MockWidget:
    """Мок для виджетов Qt."""

    def __init__(self) -> None:
        """Инициализация мока."""
        self.mock_show = MagicMock()
        self.mock_hide = MagicMock()
        self.mock_set_text = MagicMock()
        self.mock_update_time = MagicMock()
        self.mock_set_focus = MagicMock()
        self.mock_activate_window = MagicMock()
        self._size = QSize(150, 50)

    def size(self) -> QSize:
        """Возвращаем фиксированный размер для тестов."""
        return self._size

    def show(self) -> None:
        """Показ виджета."""
        self.mock_show()

    def hide(self) -> None:
        """Скрытие виджета."""
        self.mock_hide()

    def setText(self, text: str) -> None:
        """Установка текста."""
        self.mock_set_text(text)

    def update_time(self, remaining: timedelta) -> None:
        """Обновление времени."""
        self.mock_update_time(remaining)

    def setFocus(self, reason: Qt.FocusReason = Qt.FocusReason.OtherFocusReason) -> None:
        """Установка фокуса."""
        self.mock_set_focus(reason)

    def activateWindow(self) -> None:
        """Активация окна."""
        self.mock_activate_window()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        """Обработка нажатий клавиш."""

    def move(self, pos: QPoint) -> None:
        """Перемещение виджета."""


class MockBlockingOverlay(MockWidget):
    """Мок для BlockingOverlay."""

    def __init__(self) -> None:
        """Инициализация мока."""
        super().__init__()


class MockTimerWidget(MockWidget):
    """Мок для TimerWidget."""

    def __init__(self) -> None:
        """Инициализация мока."""
        super().__init__()


# Создаем моки для PyQt6
qt_core = MagicMock()
qt_core.Qt = Qt
qt_core.QTimer = MagicMock()

qt_gui = MagicMock()
qt_gui.QIcon = MagicMock()
qt_gui.QPainter = MagicMock()
qt_gui.QColor = MagicMock()
qt_gui.QKeyEvent = QKeyEvent

qt_widgets = MagicMock()
qt_widgets.QApplication = MagicMock()
qt_widgets.QSystemTrayIcon = MagicMock()
qt_widgets.QMenu = MagicMock()
qt_widgets.QWidget = QWidget
qt_widgets.QLabel = QLabel
qt_widgets.QVBoxLayout = QVBoxLayout

# Патчим модули PyQt6
with patch.dict(
    "sys.modules",
    {
        "PyQt6.QtCore": qt_core,
        "PyQt6.QtGui": qt_gui,
        "PyQt6.QtWidgets": qt_widgets,
    },
):
    from take_break.app import TakeBreakApp


class TestTakeBreakApp(unittest.TestCase):
    """Тесты для основного класса приложения."""

    def setUp(self) -> None:
        """Подготовка к тестам."""
        # Создаем экземпляр QApplication перед всеми тестами
        self.qapp = QApplication([])

        # Создаем моки
        self.blocker_mock = MagicMock()
        self.overlay_mock = MockBlockingOverlay()
        self.timer_widget_mock = MockTimerWidget()

        # Патчим все что движется
        with (
            patch("take_break.app.InputBlocker", return_value=self.blocker_mock),
            patch("take_break.app.BlockingOverlay", return_value=self.overlay_mock),
            patch("take_break.app.TimerWidget", return_value=self.timer_widget_mock),
            patch("take_break.app.QTimer"),
            patch("take_break.app.QApplication"),
        ):
            self.take_break = TakeBreakApp()

    def test_initial_state(self) -> None:
        """Тест начального состояния приложения."""
        self.assertEqual(self.take_break.work_duration, 25)
        self.assertEqual(self.take_break.break_duration, 5)

    def test_handle_key_press_up(self) -> None:
        """Тест обработки нажатия клавиши вверх."""
        event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier)
        self.take_break.overlay.keyPressEvent(event)
        self.assertEqual(self.take_break.work_duration, 30)

    def test_handle_key_press_down(self) -> None:
        """Тест обработки нажатия клавиши вниз."""
        self.take_break.work_duration = 30
        event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
        self.take_break.overlay.keyPressEvent(event)
        self.assertEqual(self.take_break.work_duration, 25)

    def test_handle_key_press_up_limit(self) -> None:
        """Тест ограничения максимального времени работы."""
        self.take_break.work_duration = 60
        event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier)
        self.take_break.overlay.keyPressEvent(event)
        self.assertEqual(self.take_break.work_duration, 60)

    def test_handle_key_press_down_limit(self) -> None:
        """Тест ограничения минимального времени работы."""
        self.take_break.work_duration = 25
        event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
        self.take_break.overlay.keyPressEvent(event)
        self.assertEqual(self.take_break.work_duration, 25)


if __name__ == "__main__":
    unittest.main()
