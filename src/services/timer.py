"""Управление состоянием таймера работы и перерыва."""

from datetime import UTC, datetime, timedelta

from loguru import logger

from src.constants.settings import BREAK_DURATION_MIN, DEFAULT_WORK_DURATION_MIN


class TimerManager:
    """Управляет состоянием таймеров работы и перерыва."""

    def __init__(self) -> None:
        """Инициализировать менеджер таймера."""
        self.work_duration: int = DEFAULT_WORK_DURATION_MIN
        self.break_duration: int = BREAK_DURATION_MIN
        self.work_end_time: datetime | None = None
        self.break_end_time: datetime | None = None

    def start_work(self, duration: int | None = None) -> None:
        """Запустить рабочий таймер.

        Args:
            duration: Длительность работы в минутах. Если None, использует текущую.

        """
        if duration is not None:
            self.work_duration = duration

        self.work_end_time = datetime.now(UTC) + timedelta(minutes=self.work_duration)
        logger.debug(f"Рабочий таймер запущен на {self.work_duration} минут")

    def start_break(self) -> None:
        """Запустить таймер перерыва."""
        self.break_end_time = datetime.now(UTC) + timedelta(minutes=self.break_duration)
        self.work_end_time = None
        logger.debug(f"Таймер перерыва запущен на {self.break_duration} минут")

    def end_break(self) -> None:
        """Завершить таймер перерыва."""
        self.break_end_time = None
        logger.debug("Таймер перерыва завершён")

    def get_work_remaining(self) -> timedelta | None:
        """Получить оставшееся рабочее время.

        Returns:
            Оставшееся время как timedelta, или None если таймер не активен.

        """
        if self.work_end_time is None:
            return None
        return self.work_end_time - datetime.now(UTC)

    def get_break_remaining(self) -> timedelta | None:
        """Получить оставшееся время перерыва.

        Returns:
            Оставшееся время как timedelta, или None если перерыв не активен.

        """
        if self.break_end_time is None:
            return None
        return self.break_end_time - datetime.now(UTC)

    def is_work_active(self) -> bool:
        """Проверить, активен ли рабочий таймер.

        Returns:
            True если рабочий таймер активен, False иначе.

        """
        return self.work_end_time is not None

    def is_break_active(self) -> bool:
        """Проверить, активен ли таймер перерыва.

        Returns:
            True если перерыв активен, False иначе.

        """
        return self.break_end_time is not None

    def is_work_expired(self) -> bool:
        """Проверить, истёк ли рабочий таймер.

        Returns:
            True если рабочий таймер истёк, False иначе.

        """
        if self.work_end_time is None:
            return False
        return datetime.now(UTC) >= self.work_end_time

    def is_break_expired(self) -> bool:
        """Проверить, истёк ли таймер перерыва.

        Returns:
            True если перерыв истёк, False иначе.

        """
        if self.break_end_time is None:
            return False
        return datetime.now(UTC) >= self.break_end_time
