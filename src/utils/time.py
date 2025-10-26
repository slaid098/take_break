"""Time formatting utilities."""

from datetime import timedelta


def format_time(remaining: timedelta) -> str:
    """Format timedelta to MM:SS string format.

    Args:
        remaining: Time delta to format.

    Returns:
        Formatted time string as MM:SS.

    """
    minutes = int(remaining.total_seconds() // 60)
    seconds = int(remaining.total_seconds() % 60)
    return f"{minutes:02d}:{seconds:02d}"

