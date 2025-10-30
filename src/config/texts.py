"""Text constants for all application messages and UI elements."""

from src.constants.settings import BREAK_DURATION_MIN, DEFAULT_WORK_DURATION_MIN


class AppInfo:
    """Application information texts."""

    TITLE = "Take Break"


class WelcomeDialog:
    """Welcome dialog texts."""

    TITLE = "Добро пожаловать в Take Break!"
    SUBTITLE = "Защита здоровья и сохранения фокуса при работе за компьютером"
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
        <div style='background-color: white; padding: 20px; border-radius: 8px; box-sizing: border-box;'>
            <p style='font-size: 15px; line-height: 1.8; margin: 0 0 10px 0; color: #34495e;'>
                <b style='color: #2c3e50; font-size: 16px;'>
                    Ключевые принципы Take Break:
                </b>
            </p>
            <ul style='font-size: 14px; color: #34495e; margin: 0; padding: 0 0 0 20px; list-style-type: disc; line-height: 1.5;'>
                <li style='margin: 0 0 10px 0; padding: 0; line-height: 1;'>
                    <b>Определяйте фокус:</b> Устанавливайте ключевую задачу на следующую сессию, чтобы возвращаться к работе было легко.
                </li>
                <li style='margin: 0 0 10px 0; padding: 0; line-height: 1;'>
                    <b>Работайте строго, отдыхайте свободно:</b> Таймер работы неотвратим, но после обязательного 5-минутного перерыва он будет ждать вашего возвращения.
                </li>
                <li style='margin: 0 0 10px 0; padding: 0; line-height: 1;'>
                    <b>Отдыхайте красиво:</b> Наслаждайтесь новыми фоновыми заставками во время каждого перерыва.
                </li>
                <li style='margin: 0; padding: 0; line-height: 1;'>
                    <b>Вы контролируете ситуацию:</b> Выход из приложения доступен в любой момент до начала перерыва.
                </li>
            </ul>
        </div>
        """  # noqa: E501

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
        previous_focus: str | None = None,
        work_duration: int | None = None,
    ) -> str:
        """Get the initial overlay text.

        Args:
            previous_focus: The previous focus text, if any.
            work_duration: The selected work duration in minutes.

        Returns:
            Initial overlay message with HTML formatting.

        """
        # If work_duration not provided, use default
        duration = work_duration if work_duration is not None else DEFAULT_WORK_DURATION_MIN
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
        return f"Break: {BREAK_DURATION_MIN} minutes"


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
