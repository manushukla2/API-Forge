from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QLineEdit, QComboBox, QFrame, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS
from ui.components.file_dropzone import FileDropzone


class DocInputScreen(QWidget):
    start_testing = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = ""
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Header
        title = QLabel("📄 Import Your API")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        sub = QLabel("Choose how you want to provide your API — we support 7 input types")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(sub)

        # Input type selector
        type_row = QHBoxLayout()
        type_label = QLabel("Input Type:")
        type_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        type_label.setFixedWidth(100)
        type_row.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Auto Detect",
            "Swagger / OpenAPI",
            "Postman Collection",
            "PDF Documentation",
            "cURL Command",
            "Base URL",
            "Plain Text"
        ])
        self.type_combo.setFixedHeight(40)
        self.type_combo.currentIndexChanged.connect(self._on_type_change)
        type_row.addWidget(self.type_combo)
        layout.addLayout(type_row)

        # File dropzone
        self.dropzone = FileDropzone([".json", ".yaml", ".yml", ".pdf"])
        self.dropzone.file_selected.connect(self._on_file)
        layout.addWidget(self.dropzone)

        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Or paste URL / cURL command / API description here...")
        self.text_input.setFixedHeight(100)
        self.text_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
                padding:          10px;
                font-size:        {FONTS['size_sm']}px;
            }}
            QTextEdit:focus {{
                border-color: {COLORS['accent']};
            }}
        """)
        layout.addWidget(self.text_input)

        # Auth config
        auth_frame = QFrame()
        auth_frame.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px;")
        auth_layout = QVBoxLayout(auth_frame)
        auth_layout.setContentsMargins(16, 12, 16, 12)
        auth_layout.setSpacing(10)

        auth_title = QLabel("🔐 Authentication (Optional)")
        auth_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        auth_layout.addWidget(auth_title)

        auth_row = QHBoxLayout()

        self.auth_type = QComboBox()
        self.auth_type.addItems(["None", "Bearer Token", "API Key", "Basic Auth"])
        self.auth_type.setFixedHeight(36)
        auth_row.addWidget(self.auth_type)

        self.auth_value = QLineEdit()
        self.auth_value.setPlaceholderText("Token / API Key value...")
        self.auth_value.setFixedHeight(36)
        auth_row.addWidget(self.auth_value)

        auth_layout.addLayout(auth_row)
        layout.addWidget(auth_frame)

        layout.addStretch()

        # Start button
        self.start_btn = QPushButton("🚀 Start Testing")
        self.start_btn.setFixedHeight(48)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color:            white;
                border:           none;
                border-radius:    10px;
                font-size:        {FONTS['size_md']}px;
                font-weight:      700;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
        """)
        self.start_btn.clicked.connect(self._on_start)
        layout.addWidget(self.start_btn)

    def _on_file(self, path: str):
        self._source = path
        self.text_input.setPlainText(path)

    def _on_type_change(self, idx: int):
        file_types = [1, 2, 3]
        if idx in file_types:
            self.dropzone.show()
        else:
            self.dropzone.hide()

    def _on_start(self):
        source = self._source or self.text_input.toPlainText().strip()
        if not source:
            return

        auth_map = {
            "None":         {"type": "none"},
            "Bearer Token": {"type": "bearer",  "token": self.auth_value.text()},
            "API Key":      {"type": "api_key", "key": "X-API-Key", "value": self.auth_value.text()},
            "Basic Auth":   {"type": "basic",   "username": self.auth_value.text()}
        }
        auth = auth_map.get(self.auth_type.currentText(), {"type": "none"})
        self.start_testing.emit(source, auth)
