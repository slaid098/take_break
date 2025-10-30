"""Timer state management service."""

from datetime import UTC, datetime, timedelta

from loguru import logger

from src.constants.settings import BREAK_DURATION_MIN, DEFAULT_WORK_DURATION_MIN


class TimerManager:
    """Manages work and break timer state."""

    def __init__(self) -> None:
        """Initialize the timer manager."""
        self.work_duration: int = DEFAULT_WORK_DURATION_MIN
        self.break_duration: int = BREAK_DURATION_MIN
        self.work_end_time: datetime | None = None
        self.break_end_time: datetime | None = None

    def start_work(self, duration: int | None = None) -> None:
        """Start the work timer.

        Args:
            duration: Work duration in minutes. If None, uses current work_duration.

        """
        if duration is not None:
            self.work_duration = duration

        self.work_end_time = datetime.now(UTC) + timedelta(minutes=self.work_duration)
        logger.debug(f"Work timer started for {self.work_duration} minutes")

    def start_break(self) -> None:
        """Start the break timer."""
        self.break_end_time = datetime.now(UTC) + timedelta(minutes=self.break_duration)
        self.work_end_time = None
        logger.debug(f"Break timer started for {self.break_duration} minutes")

    def end_break(self) -> None:
        """End the break timer."""
        self.break_end_time = None
        logger.debug("Break timer ended")

    def get_work_remaining(self) -> timedelta | None:
        """Get remaining work time.

        Returns:
            Remaining time as timedelta, or None if work timer is not active.

        """
        if self.work_end_time is None:
            return None
        return self.work_end_time - datetime.now(UTC)

    def get_break_remaining(self) -> timedelta | None:
        """Get remaining break time.

        Returns:
            Remaining time as timedelta, or None if break timer is not active.

        """
        if self.break_end_time is None:
            return None
        return self.break_end_time - datetime.now(UTC)

    def is_work_active(self) -> bool:
        """Check if work timer is active.

        Returns:
            True if work timer is active, False otherwise.

        """
        return self.work_end_time is not None

    def is_break_active(self) -> bool:
        """Check if break timer is active.

        Returns:
            True if break timer is active, False otherwise.

        """
        return self.break_end_time is not None

    def is_work_expired(self) -> bool:
        """Check if work timer has expired.

        Returns:
            True if work timer is expired, False otherwise.

        """
        if self.work_end_time is None:
            return False
        return datetime.now(UTC) >= self.work_end_time

    def is_break_expired(self) -> bool:
        """Check if break timer has expired.

        Returns:
            True if break timer is expired, False otherwise.

        """
        if self.break_end_time is None:
            return False
        return datetime.now(UTC) >= self.break_end_time

