from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


class TopBar(QWidget):
    settings_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(56)
        self.setStyleSheet(f"background-color: {COLORS['topbar_bg']}; border-bottom: 1px solid {COLORS['border']};")
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        self.title = QLabel("Home")
        self.title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_lg']}px; font-weight: 700;")
        layout.addWidget(self.title)

        layout.addStretch()

        self.status = QLabel("")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(self.status)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setObjectName("ghost")
        settings_btn.setFixedWidth(100)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(settings_btn)

    def set_title(self, title: str):
        self.title.setText(title)

    def set_status(self, msg: str, color: str = None):
        self.status.setText(msg)
        if color:
            self.status.setStyleSheet(f"color: {color}; font-size: {FONTS['size_sm']}px;")
        else:
            self.status.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
