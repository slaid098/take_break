"""Text constants for all application messages and UI elements."""

from src.config import settings


class AppInfo:
    """Application information texts."""

    TITLE = "Take Break"


class WelcomeDialog:
    """Welcome dialog texts."""

    TITLE = "Добро пожаловать в Take Break!"
    SUBTITLE = "Защита здоровья при работе за компьютером"
    BUTTON_START = "Начать работу"
    BUTTON_CANCEL = "Отмена"
    CHECKBOX_ONLINE = "Загружать случайные обои из интернета"


class WelcomeDialogTexts:
    """Welcome dialog texts with properties."""

    @property
    def description(self) -> str:
        """Get the welcome dialog description HTML.

        Returns:
            HTML formatted description text.

        """
        return """
        <div style='background-color: white; padding: 20px; border-radius: 8px;'>
            <p style='font-size: 15px; line-height: 1.8; margin: 0; color: #34495e;'>
                <b style='color: #2c3e50; font-size: 16px;'>
                    Дисциплина в работе, свобода в отдыхе
                </b>
            </p>
            <p style='font-size: 14px; line-height: 1.8; margin-top: 12px; color: #34495e;'>
                Take Break бережно защищает вас от непрерывной работы:
            </p>
            <ul style='font-size: 14px; line-height: 2; color: #34495e; margin-top: 10px;'>
                <li>Перерывы нельзя пропустить</li>
                <li>После обязательных 5 минут вы сами решаете, когда вернуться</li>
                <li>Выход из приложения доступен только во время работы</li>
            </ul>
        </div>
        """

    @property
    def checkbox_online(self) -> str:
        """Get checkbox text for online wallpapers.

        Returns:
            Checkbox text.

        """
        return WelcomeDialog.CHECKBOX_ONLINE


class Overlay:
    """Overlay window texts."""

    PLACEHOLDER = "✨ Введите ваш фокус на следующую сессию..."

    @staticmethod
    def get_initial_text(
        previous_focus: str | None = None, work_duration: int | None = None,
    ) -> str:
        """Get the initial overlay text.

        Args:
            previous_focus: The previous focus text, if any.
            work_duration: The selected work duration in minutes.

        Returns:
            Initial overlay message with HTML formatting.

        """
        # If work_duration not provided, use default
        duration = (
            work_duration if work_duration is not None
            else settings.DEFAULT_WORK_DURATION_MIN
        )
        if previous_focus:
            return (
                f"<div style='text-align: center;'>"
                f"<p style='font-size: 24px; margin-bottom: 40px; line-height: 1.4;'>"
                f"<span style='color: #ffd700; font-size: 28px;'>🎯</span> "
                f"<b>Ваш предыдущий фокус:</b><br/>"
                f"<span style='color: #00d4ff; font-size: 28px;'>{previous_focus}</span>"
                f"</p>"
                f"<p style='font-size: 16px; line-height: 2.2; color: rgba(255,255,255,0.9);'>"
                f"✨ Нажмите <b style='color: #00ff88;'>Enter</b> для продолжения "
                f"или измените фокус</p></div>"
            )
        return (
            f"<div style='text-align: center;'>"
            f"<p style='font-size: 24px; margin-bottom: 40px; line-height: 1.4;'>"
            f"<span style='font-size: 36px;'>⏱️</span><br/>"
            f"Нажмите <b style='color: #00ff88;'>Enter</b>, чтобы начать<br/>"
            f"<span style='color: #00d4ff; font-size: 28px;'>"
            f"{duration}-минутный</span> рабочий сеанс</p></div>"
        )

    @property
    def break_message(self) -> str:
        """Get the break message.

        Returns:
            Break message text.

        """
        return f"Break: {settings.BREAK_DURATION_MIN} minutes"


class WorkModes:
    """Work mode names."""

    POMODORO = "Pomodoro"
    STANDARD = "Стандартный"


class Tray:
    """System tray texts."""

    TOOLTIP_WAITING = "Take Break - Ожидание"
    TOOLTIP_WORK = "Take Break - Работа активна"
    TOOLTIP_BREAK = "Take Break - Перерыв активен"
    MENU_AUTOSTART = "Автозапуск"
    MENU_ONLINE_WALLPAPERS = "Онлайн обои"
    MENU_WORK_MODE = "Режим работы"
    MENU_MOVE_TIMER = "Переместить таймер"
    MENU_QUIT = "Выход"
    MESSAGE_INFO = "Используйте меню для управления"
    MESSAGE_TITLE = "Take Break"
