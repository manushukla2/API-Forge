from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from ui.theme import COLORS, FONTS


class Toast(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(40)
        self.hide()
        self._timer = QTimer()
        self._timer.timeout.connect(self.hide)

    def show_message(self, message: str, type: str = "info", duration: int = 3000):
        colors = {
            "info":    COLORS["accent"],
            "success": COLORS["success"],
            "error":   COLORS["danger"],
            "warning": COLORS["warning"]
        }
        bg = colors.get(type, COLORS["accent"])

        self.setText(message)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color:            white;
                border-radius:    8px;
                padding:          8px 20px;
                font-size:        {FONTS['size_sm']}px;
                font-weight:      600;
            }}
        """)
        self.show()
        self._timer.start(duration)

    def success(self, msg: str):
        self.show_message(msg, "success")

    def error(self, msg: str):
        self.show_message(msg, "error")

    def info(self, msg: str):
        self.show_message(msg, "info")

    def warning(self, msg: str):
        self.show_message(msg, "warning")
