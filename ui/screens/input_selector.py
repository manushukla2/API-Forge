from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


INPUT_OPTIONS = [
    {"key": "swagger", "icon": "📋", "title": "Swagger / OpenAPI", "desc": "Upload .json or .yaml file", "accepts": [".json", ".yaml", ".yml"]},
    {"key": "postman", "icon": "📮", "title": "Postman Collection", "desc": "Upload collection .json",   "accepts": [".json"]},
    {"key": "pdf",     "icon": "📄", "title": "PDF Documentation", "desc": "Upload API docs PDF",        "accepts": [".pdf"]},
    {"key": "curl",    "icon": "⌨️",  "title": "cURL Command",      "desc": "Paste a cURL command",       "accepts": []},
    {"key": "url",     "icon": "🌐", "title": "Base URL",           "desc": "Enter API base URL",         "accepts": []},
    {"key": "proxy",   "icon": "🔀", "title": "Live Traffic",       "desc": "Capture proxy traffic",      "accepts": []},
    {"key": "text",    "icon": "✏️",  "title": "Plain Text",         "desc": "Describe your API",          "accepts": []}
]


class InputSelector(QWidget):
    input_selected = pyqtSignal(str, str)  # type, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("How are you providing your API?")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        sub = QLabel("Choose any input type — we'll handle the rest")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(sub)

        # Grid of options
        grid = QHBoxLayout()
        grid.setSpacing(12)

        col1 = QVBoxLayout()
        col1.setSpacing(10)
        col2 = QVBoxLayout()
        col2.setSpacing(10)

        for i, opt in enumerate(INPUT_OPTIONS):
            card = self._option_card(opt)
            if i % 2 == 0:
                col1.addWidget(card)
            else:
                col2.addWidget(card)

        col1.addStretch()
        col2.addStretch()
        grid.addLayout(col1)
        grid.addLayout(col2)
        layout.addLayout(grid)

        # Input area
        self.input_area = QWidget()
        input_layout    = QVBoxLayout(self.input_area)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Paste URL, cURL command, or text here...")
        self.text_input.setFixedHeight(44)
        input_layout.addWidget(self.text_input)

        self.proceed_btn = QPushButton("Proceed →")
        self.proceed_btn.setFixedHeight(44)
        self.proceed_btn.clicked.connect(self._on_proceed)
        input_layout.addWidget(self.proceed_btn)

        self.input_area.hide()
        layout.addWidget(self.input_area)

    def _option_card(self, opt: dict) -> QFrame:
        card = QFrame()
        card.setFixedHeight(72)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
            QFrame:hover {{
                border-color: {COLORS['accent']};
                background-color: {COLORS['bg_secondary']};
            }}
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        icon = QLabel(opt["icon"])
        icon.setStyleSheet(f"font-size: 20px;")
        icon.setFixedWidth(28)
        layout.addWidget(icon)

        info = QVBoxLayout()
        info.setSpacing(2)

        t = QLabel(opt["title"])
        t.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        info.addWidget(t)

        d = QLabel(opt["desc"])
        d.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        info.addWidget(d)

        layout.addLayout(info)

        card.mousePressEvent = lambda e, o=opt: self._on_select(o)
        return card

    def _on_select(self, opt: dict):
        self._selected = opt
        self.text_input.setPlaceholderText(f"Enter {opt['title']}...")
        self.input_area.show()

    def _on_proceed(self):
        if self._selected and self.text_input.text().strip():
            self.input_selected.emit(
                self._selected["key"],
                self.text_input.text().strip()
            )
