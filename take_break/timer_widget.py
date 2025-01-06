"""Модуль для отображения виджета таймера."""

from datetime import timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TimerWidget(QWidget):
    """Виджет для отображения таймера."""

    def __init__(self) -> None:
        """Инициализация виджета таймера."""
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Настройка интерфейса
        layout = QVBoxLayout()
        self.time_label = QLabel()
        self.reset_style()
        layout.addWidget(self.time_label)
        self.setLayout(layout)

        # Устанавливаем размер и позицию
        self.resize(150, 50)
        screen = self.screen().geometry()
        self.move(screen.width() - 170, 20)

    def reset_style(self) -> None:
        """Сброс стиля к исходному состоянию."""
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 180);
                padding: 10px;
                border-radius: 5px;
            }
        """)

    def update_time(self, remaining: timedelta) -> None:
        """Обновление отображаемого времени."""
        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)

        # Окрашиваем в красный, если осталась минута
        if remaining.total_seconds() <= 60:
            self.time_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    background-color: rgba(255, 0, 0, 180);
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
        else:
            self.reset_style()

        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
