"""Тесты утилиты форматирования времени."""

from datetime import timedelta

import pytest
from src.utils.time import format_time


class TestFormatTime:
    """Тесты функции format_time."""

    @pytest.mark.parametrize(
        ("seconds", "expected"),
        [
            (0, "00:00"),
            (5, "00:05"),
            (30, "00:30"),
            (60, "01:00"),
            (90, "01:30"),
            (125, "02:05"),
            (3600, "60:00"),
            (3661, "61:01"),
        ],
    )
    def test_format_time(self, seconds: int, expected: str) -> None:
        """format_time форматирует timedelta корректно."""
        assert format_time(timedelta(seconds=seconds)) == expected

    def test_format_time_zero(self) -> None:
        """format_time форматирует нулевой timedelta."""
        assert format_time(timedelta(0)) == "00:00"
