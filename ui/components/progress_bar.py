from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS


class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Top row — label + percent
        top = QHBoxLayout()
        self.label = QLabel("Ready")
        self.label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")

        self.percent = QLabel("0%")
        self.percent.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)

        top.addWidget(self.label)
        top.addWidget(self.percent)
        layout.addLayout(top)

        # Progress bar
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(6)
        layout.addWidget(self.bar)

    def update(self, message: str, value: int):
        self.label.setText(message)
        self.percent.setText(f"{value}%")
        self.bar.setValue(value)

        if value == 100:
            self.bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {COLORS['success']}; border-radius: 3px; }}")
        else:
            self.bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {COLORS['accent']}; border-radius: 3px; }}")

    def reset(self):
        self.update("Ready", 0)
        self.bar.setStyleSheet("")
