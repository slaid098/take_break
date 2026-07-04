"""Оркестратор приложения Take Break."""

import sys
from datetime import UTC, datetime

import keyboard
from loguru import logger
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QDialog

from src.config import texts
from src.config.settings import Settings
from src.constants.settings import (
    BREAK_DURATION_MIN,
    MOVE_TIMER_HOTKEY,
    POMODORO_MODE_MIN,
    TIMER_INTERVAL_MS,
)
from src.db.db import Database
from src.services import autostart
from src.services.position import (
    WidgetPosition,
    calculate_position,
    get_next_position,
)
from src.services.timer import TimerManager
from src.widgets.overlay import BlockingOverlay
from src.widgets.timer import TimerWidget
from src.widgets.tray import SystemTray
from src.widgets.welcome import WelcomeDialog


class App:
    """Оркестратор приложения.

    Координирует взаимодействие между сервисами и виджетами,
    не содержа бизнес-логики. Знает КОГДА вызывать методы, но не КАК они работают.
    """

    def __init__(self) -> None:
        """Инициализировать приложение.

        Создаёт QApplication, инициализирует все компоненты
        и связывает сигналы между ними.
        """
        logger.debug("Инициализация приложения")
        self.app = QApplication(sys.argv)
        self.width = self.app.primaryScreen().geometry().width()
        self.height = self.app.primaryScreen().geometry().height()

        self.overlay = BlockingOverlay(screen_width=self.width, screen_height=self.height)
        self.timer_manager = TimerManager()
        self.settings = Settings(db=Database())

        self.timer_widget = TimerWidget()
        self.tray = SystemTray()

        self.current_position = WidgetPosition.TOP_RIGHT

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_timeout)

        self.focus_text = self.settings.get_focus()
        self.work_duration = self.settings.get_work_duration()

        self._extra_rest_start: datetime | None = None

        self.overlay.close_requested.connect(self.quit)
        self.overlay.enter_pressed.connect(self._on_enter_pressed)

        self._setup_hotkeys()
        self._setup_tray()

        use_online = self.settings.get_use_online_wallpapers()
        self.overlay.wallpaper_manager.set_use_online(use_online)
        self.tray.set_online_wallpapers_enabled(use_online)

        if self.settings.is_first_run():
            self._show_welcome_dialog()

        self.show_initial_overlay()
        self.tray.show()

        logger.info("Приложение инициализировано и готово к работе")

    def _setup_hotkeys(self) -> None:
        """Настроить глобальные хоткеи приложения."""
        hotkey = self.settings.get_move_timer_hotkey()
        if not hotkey:
            hotkey = MOVE_TIMER_HOTKEY
            self.settings.set_move_timer_hotkey(hotkey)
        keyboard.add_hotkey(hotkey, self._move_timer)

    def _setup_tray(self) -> None:
        """Настроить сигналы системного трея и начальное состояние."""
        self.tray.quit_requested.connect(self.quit)
        self.tray.autostart_toggled.connect(self._on_autostart_toggle)
        self.tray.online_wallpapers_toggled.connect(self._on_online_wallpapers_toggle)
        self.tray.work_mode_changed.connect(self._on_work_mode_changed)
        self.tray.move_timer_requested.connect(self._move_timer)

        self.tray.set_autostart_enabled(autostart.is_autostart_enabled())
        self.tray.set_work_mode(self.work_duration)
        self._update_tray_state()

    def _show_welcome_dialog(self) -> None:
        """Показать диалог приветствия при первом запуске."""
        dialog = WelcomeDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Rejected:
            logger.info("Пользователь отказался запускать приложение")
            self.quit()
            sys.exit(0)

        selected_duration = dialog.get_selected_work_duration()
        self.settings.set_work_duration(selected_duration)
        self.work_duration = selected_duration
        self.tray.set_work_mode(selected_duration)

        self.settings.mark_first_run_complete()
        logger.info("Диалог приветствия принят, первый запуск отмечен")

    def _on_autostart_toggle(self, enabled: bool) -> None:
        """Обработать переключение автозапуска из трея.

        Args:
            enabled: True для включения, False для отключения.

        """
        if enabled:
            autostart.enable_autostart()
        else:
            autostart.disable_autostart()
        logger.info(f"Автозапуск переключён: {enabled}")

    def _on_online_wallpapers_toggle(self, enabled: bool) -> None:
        """Обработать переключение онлайн-обоев из трея.

        Args:
            enabled: True для включения онлайн-обоев.

        """
        self.settings.set_use_online_wallpapers(enabled)
        self.overlay.wallpaper_manager.set_use_online(enabled)
        logger.info(f"Онлайн-обои переключены: {enabled}")

    def _on_work_mode_changed(self, duration: int) -> None:
        """Обработать смену рабочего режима из трея.

        Args:
            duration: Длительность в минутах (25 или 45).

        """
        self.work_duration = duration
        self.settings.set_work_duration(duration)
        self.tray.set_work_mode(duration)

        mode_name = (
            texts.WorkModes.POMODORO if duration == POMODORO_MODE_MIN else texts.WorkModes.STANDARD
        )
        message = f"Режим изменён на {duration} мин ({mode_name}). Применится после текущего цикла"
        self.tray.showMessage(
            texts.Tray.MESSAGE_TITLE,
            message,
            self.tray.MessageIcon.Information,
            3000,
        )
        logger.info(f"Рабочий режим изменён на {duration} минут")

    def _update_tray_state(self) -> None:
        """Обновить иконку и меню трея на основе текущего состояния таймера."""
        is_work_active = self.timer_manager.is_work_active()
        is_break_active = self.timer_manager.is_break_active()
        self.tray.update_state(is_work_active, is_break_active)

    def _move_timer(self) -> None:
        """Сменить позицию таймера на экране."""
        self.current_position = get_next_position(self.current_position)
        self._reposition_timer()
        logger.debug(f"Таймер перемещён: {self.current_position.name}")

    def _reposition_timer(self) -> None:
        """Разместить виджет таймера на экране."""
        if not (screen := self.app.primaryScreen()):
            return

        screen_geometry = screen.availableGeometry()
        widget_size = self.timer_widget.size()

        position = calculate_position(
            self.current_position,
            screen_geometry.width(),
            screen_geometry.height(),
            widget_size.width(),
            widget_size.height(),
        )

        x = screen_geometry.x() + position.x()
        y = screen_geometry.y() + position.y()

        self.timer_widget.move(x, y)

    def show_initial_overlay(self) -> None:
        """Показать начальный overlay для выбора рабочего режима."""
        overlay_text = texts.Overlay.get_initial_text(
            self.focus_text if self.focus_text else None,
            self.work_duration,
        )
        self.overlay.set_text(overlay_text)

        if self.focus_text:
            self.overlay.set_focus_text(self.focus_text)

        self.overlay.show_focus_input()

        if self._extra_rest_start:
            self.overlay.show_extra_rest_timer(self._extra_rest_start)

        self.overlay.show()

    def _on_enter_pressed(self) -> None:
        """Обработать нажатие Enter на overlay.

        Сохраняет фокус и запускает рабочий таймер.
        Игнорируется во время перерыва.
        """
        if self.timer_manager.is_break_active():
            logger.warning("Нельзя начать работу во время перерыва")
            return

        self.focus_text = self.overlay.get_focus_text()
        self.settings.save_focus(self.focus_text)
        self.overlay.hide()
        self.start_work_timer()
        logger.info(f"Рабочий таймер запущен с фокусом: {self.focus_text}")

    def start_work_timer(self) -> None:
        """Запустить рабочий таймер."""
        if self.timer_manager.is_break_active():
            logger.warning("Попытка запустить таймер во время перерыва")
            return

        self.work_duration = self.settings.get_work_duration()
        self._extra_rest_start = None

        self.timer_manager.start_work(self.work_duration)
        self.timer_widget.set_focus_text(self.focus_text)
        self.timer_widget.show()

        QTimer.singleShot(0, self._reposition_timer)

        self.timer.start(TIMER_INTERVAL_MS)
        self._update_tray_state()
        logger.info(f"Рабочий таймер запущен на {self.work_duration} минут")

    def start_break_timer(self) -> None:
        """Запустить таймер перерыва."""
        self.timer_manager.start_break()
        self.overlay.is_blocking = True
        self.overlay.hide_focus_input()
        self.overlay.hide_extra_rest_timer()
        self.overlay.set_text(texts.Overlay.break_message())
        self.overlay.show()
        self._update_tray_state()
        logger.info(f"Перерыв начат на {BREAK_DURATION_MIN} минут")

    def _on_timer_timeout(self) -> None:
        """Обновить UI на основе состояния таймера."""
        if self.timer_manager.is_work_expired():
            logger.debug("Рабочее время истекло")
            self.start_break_timer()
        elif self.timer_manager.is_work_active():
            remaining = self.timer_manager.get_work_remaining()
            if remaining:
                self.timer_widget.update_time(remaining)

        if self.timer_manager.is_break_expired():
            logger.debug("Перерыв истёк")
            self.end_break()
        elif self.timer_manager.is_break_active():
            remaining = self.timer_manager.get_break_remaining()
            if remaining:
                self.overlay.update_time(remaining)

    def end_break(self) -> None:
        """Завершить перерыв и вернуться в начальное состояние."""
        self.timer_manager.end_break()
        self._extra_rest_start = datetime.now(UTC)

        self.overlay.is_blocking = False
        self.overlay.show_focus_input()
        self.overlay.hide()
        self.timer_widget.hide()
        self.timer_widget.reset_style()
        self.timer.stop()
        self._update_tray_state()
        self.show_initial_overlay()
        logger.info("Перерыв завершён, запущен таймер доп. отдыха")

    def quit(self) -> None:
        """Выйти из приложения.

        Блокирует выход во время активного перерыва.
        """
        if self.timer_manager.is_break_active():
            logger.warning("Нельзя выйти во время перерыва")
            return
        keyboard.unhook_all()
        self.app.quit()

    def run(self) -> int:
        """Запустить главный цикл приложения.

        Returns:
            Код выхода приложения.

        """
        return self.app.exec()
