"""Take Break - приложение для принудительных перерывов во время работы за компьютером."""

__version__ = "0.1.0"

from .app import TakeBreakApp
from .blocker import InputBlocker
from .overlay import BlockingOverlay
from .timer_widget import TimerWidget

__all__ = ["BlockingOverlay", "InputBlocker", "TakeBreakApp", "TimerWidget"]
