"""Хранилище настроек приложения."""

from loguru import logger

from src.constants.settings import (
    AVAILABLE_WORK_MODES,
    DEFAULT_WORK_DURATION_MIN,
    LOAD_IMAGE_TIMEOUT_DEFAULT,
)
from src.db.db import Database
from src.schemas.settings import SettingsKey


class Settings:
    """Управление постоянными настройками через SQLite."""

    def __init__(self, db: Database) -> None:
        """Инициализировать хранилище настроек.

        Args:
            db: Экземпляр базы данных.

        """
        self.db = db
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        """Заполнить значения по умолчанию если их нет в базе."""
        defaults: dict[str, str | int | bool] = {
            SettingsKey.FOCUS: "",
            SettingsKey.FIRST_RUN_COMPLETE: "false",
            SettingsKey.USE_ONLINE_WALLPAPERS: "true",
            SettingsKey.WORK_DURATION: str(DEFAULT_WORK_DURATION_MIN),
            SettingsKey.MOVE_TIMER_HOTKEY: "",
            SettingsKey.LOAD_IMAGE_TIMEOUT: str(LOAD_IMAGE_TIMEOUT_DEFAULT),
        }

        for key, value in defaults.items():
            if self.db.get(key) is None:
                self.db.set(key, value=value)

    def get_focus(self) -> str:
        """Получить сохранённый фокус.

        Returns:
            Сохранённый фокус или пустая строка.

        """
        return self.db.get(SettingsKey.FOCUS, "") or ""

    def save_focus(self, focus: str) -> None:
        """Сохранить фокус.

        Args:
            focus: Текст фокуса для сохранения.

        """
        self.db.set(SettingsKey.FOCUS, value=focus)
        logger.debug(f"Фокус сохранён: {focus}")

    def is_first_run(self) -> bool:
        """Проверить, первый ли это запуск приложения.

        Returns:
            True если первый запуск, False иначе.

        """
        return not self.db.get_bool(SettingsKey.FIRST_RUN_COMPLETE, default=False)

    def mark_first_run_complete(self) -> None:
        """Отметить первый запуск как завершённый."""
        self.db.set(SettingsKey.FIRST_RUN_COMPLETE, value=True)
        logger.debug("Первый запуск отмечен как завершённый")

    def get_use_online_wallpapers(self) -> bool:
        """Получить настройку онлайн-обоев.

        Returns:
            Использовать ли онлайн-обои.

        """
        return self.db.get_bool(SettingsKey.USE_ONLINE_WALLPAPERS, default=True)

    def set_use_online_wallpapers(self, enabled: bool) -> None:
        """Установить настройку онлайн-обоев.

        Args:
            enabled: Включить ли онлайн-обои.

        """
        self.db.set(SettingsKey.USE_ONLINE_WALLPAPERS, value=enabled)
        logger.debug(f"Онлайн-обои: {enabled}")

    def get_work_duration(self) -> int:
        """Получить длительность рабочего режима.

        Returns:
            Длительность в минутах (25 или 45).

        """
        return self.db.get_int(SettingsKey.WORK_DURATION, DEFAULT_WORK_DURATION_MIN)

    def set_work_duration(self, duration: int) -> None:
        """Установить длительность рабочего режима.

        Args:
            duration: Длительность в минутах (25 или 45).

        """
        if duration not in AVAILABLE_WORK_MODES:
            logger.warning(
                f"Некорректная длительность: {duration}, использую {DEFAULT_WORK_DURATION_MIN}"
            )
            duration = DEFAULT_WORK_DURATION_MIN

        self.db.set(SettingsKey.WORK_DURATION, value=duration)
        logger.debug(f"Длительность работы: {duration} минут")

    def get_move_timer_hotkey(self) -> str:
        """Получить хоткей перемещения таймера.

        Returns:
            Сохранённый хоткей или пустая строка.

        """
        return self.db.get(SettingsKey.MOVE_TIMER_HOTKEY, "") or ""

    def set_move_timer_hotkey(self, hotkey: str) -> None:
        """Сохранить хоткей перемещения таймера.

        Args:
            hotkey: Хоткей (например, "ctrl+alt+t").

        """
        self.db.set(SettingsKey.MOVE_TIMER_HOTKEY, value=hotkey)
        logger.debug(f"Хоткей перемещения таймера: {hotkey}")

    def get_load_image_timeout(self) -> int:
        """Получить таймаут загрузки изображений.

        Returns:
            Таймаут в секундах.

        """
        return self.db.get_int(SettingsKey.LOAD_IMAGE_TIMEOUT, LOAD_IMAGE_TIMEOUT_DEFAULT)

    def set_load_image_timeout(self, timeout: int) -> None:
        """Установить таймаут загрузки изображений.

        Args:
            timeout: Таймаут в секундах.

        """
        self.db.set(SettingsKey.LOAD_IMAGE_TIMEOUT, value=timeout)
        logger.debug(f"Таймаут загрузки изображений: {timeout} сек")
