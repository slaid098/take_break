"""Тесты менеджера таймера."""

from datetime import UTC, datetime, timedelta

import pytest
from src.services.timer import TimerManager


class TestTimerManager:
    """Тесты менеджера таймера работы и перерыва."""

    @pytest.fixture
    def manager(self) -> TimerManager:
        """Создать менеджер таймера."""
        return TimerManager()

    def test_initial_state_no_active_timers(self, manager: TimerManager) -> None:
        """В начальном состоянии ни один таймер не активен."""
        assert not manager.is_work_active()
        assert not manager.is_break_active()
        assert manager.get_work_remaining() is None
        assert manager.get_break_remaining() is None

    def test_start_work_activates_work_timer(self, manager: TimerManager) -> None:
        """Запуск работы активирует рабочий таймер."""
        manager.start_work(25)

        assert manager.is_work_active()
        assert not manager.is_break_active()
        assert manager.get_work_remaining() is not None
        assert manager.get_work_remaining() > timedelta(0)

    def test_start_work_with_none_uses_default_duration(self, manager: TimerManager) -> None:
        """Запуск с duration=None использует текущую длительность."""
        manager.start_work(45)
        manager.start_work(None)

        assert manager.is_work_active()
        assert manager.work_duration == 45

    def test_start_break_deactivates_work(self, manager: TimerManager) -> None:
        """Запуск перерыва деактивирует рабочий таймер."""
        manager.start_work(25)
        assert manager.is_work_active()

        manager.start_break()

        assert not manager.is_work_active()
        assert manager.is_break_active()
        assert manager.get_break_remaining() is not None
        assert manager.get_break_remaining() > timedelta(0)

    def test_end_break_deactivates_break(self, manager: TimerManager) -> None:
        """Завершение перерыва деактивирует таймер перерыва."""
        manager.start_break()
        assert manager.is_break_active()

        manager.end_break()

        assert not manager.is_break_active()
        assert manager.get_break_remaining() is None

    def test_is_work_expired_false_when_active(self, manager: TimerManager) -> None:
        """Рабочий таймер не истёк пока активен."""
        manager.start_work(25)

        assert not manager.is_work_expired()

    def test_is_work_expired_false_when_not_started(self, manager: TimerManager) -> None:
        """Рабочий таймер не истёк если не запущен."""
        assert not manager.is_work_expired()

    def test_is_break_expired_false_when_not_started(self, manager: TimerManager) -> None:
        """Таймер перерыва не истёк если не запущен."""
        assert not manager.is_break_expired()

    def test_start_work_sets_correct_end_time(self, manager: TimerManager) -> None:
        """Запуск работы устанавливает корректное время окончания."""
        before = datetime.now(UTC)
        manager.start_work(25)
        after = datetime.now(UTC)

        expected_min = before + timedelta(minutes=25)
        expected_max = after + timedelta(minutes=25)

        assert manager.work_end_time is not None
        assert expected_min <= manager.work_end_time <= expected_max

    def test_is_break_expired_false_when_active(self, manager: TimerManager) -> None:
        """Таймер перерыва не истёк пока активен."""
        manager.start_break()
        assert not manager.is_break_expired()

    def test_start_break_sets_correct_duration(self, manager: TimerManager) -> None:
        """Запуск перерыва устанавливает длительность 5 минут."""
        manager.start_break()
        remaining = manager.get_break_remaining()
        assert remaining is not None
        assert remaining > timedelta(minutes=4, seconds=55)
        assert remaining <= timedelta(minutes=5)

    def test_full_work_break_cycle(self, manager: TimerManager) -> None:
        """Полный цикл: работа → перерыв → завершение."""
        manager.start_work(25)
        assert manager.is_work_active()
        assert not manager.is_break_active()

        manager.start_break()
        assert not manager.is_work_active()
        assert manager.is_break_active()

        manager.end_break()
        assert not manager.is_break_active()
        assert not manager.is_work_active()
