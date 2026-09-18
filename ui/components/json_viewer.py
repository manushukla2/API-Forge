from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont
from ui.theme import COLORS
import json


class JsonViewer(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 11))
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['bg_input']};
                color:            #e2e8f0;
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
                padding:          12px;
            }}
        """)

    def load(self, data):
        if isinstance(data, (dict, list)):
            text = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            text = str(data)
        self.setPlainText(text)

    def clear_view(self):
        self.setPlainText("")
