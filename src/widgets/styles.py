"""UI styles for widgets."""

EXTRA_REST_LABEL_STYLE = """
    QLabel {
        color: rgba(255, 215, 0, 1.0);
        font-size: 18px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(0, 0, 0, 150);
    }
"""


# Overlay window styles
OVERLAY_LABEL_STYLE = """
    QLabel {
        color: white;
        font-size: 24px;
        font-weight: 500;
        padding: 30px 40px;
        background-color: rgba(20, 20, 30, 220);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        max-width: 700px;
    }
"""

OVERLAY_INPUT_STYLE = """
    QLineEdit {
        color: white;
        font-size: 20px;
        border: 2px solid white;
        border-radius: 10px;
        padding: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(0, 0, 0, 150);
    }
"""

# Timer widget styles
TIMER_WIDGET_STYLE = """
    QWidget {
        background-color: rgba(0, 0, 0, 150);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 20);
    }
"""

TIMER_TIME_STYLE = """
    QLabel {
        font-size: 18px;
        color: white;
        font-weight: bold;
        padding: 8px 12px;
        background: transparent;
    }
"""

TIMER_TIME_RED_STYLE = """
    QLabel {
        font-size: 18px;
        color: white;
        font-weight: bold;
        padding: 8px 12px;
        background-color: rgba(200, 50, 50, 150);
    }
"""

TIMER_FOCUS_STYLE = """
    QLabel {
        font-size: 13px;
        color: rgba(255, 255, 255, 150);
        padding: 4px 12px;
        background: transparent;
    }
"""


# Welcome dialog styles
WELCOME_DIALOG_STYLE = """
    QDialog {
        background-color: #f5f5f5;
    }
"""

WELCOME_TITLE_STYLE = """
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
"""

WELCOME_SUBTITLE_STYLE = """
    font-size: 16px;
    color: #7f8c8d;
    margin-bottom: 20px;
"""

WELCOME_DESCRIPTION_STYLE = """
    QLabel {
        background-color: white;
        border-radius: 14px;
        padding: 5px;
    }
"""

WELCOME_BUTTONS_STYLE = """
    QPushButton {
        font-size: 14px;
        padding: 10px 20px;
        border-radius: 5px;
        min-width: 120px;
    }
    QPushButton:default {
        background-color: #3498db;
        color: white;
        border: none;
    }
    QPushButton:default:hover {
        background-color: #2980b9;
    }
    QPushButton:!default {
        background-color: #ecf0f1;
        color: #34495e;
        border: 1px solid #bdc3c7;
    }
    QPushButton:!default:hover {
        background-color: #d5dbdb;
    }
"""
