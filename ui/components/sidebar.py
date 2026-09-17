from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


class Sidebar(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setObjectName("sidebar")
        self.setStyleSheet(f"background-color: {COLORS['sidebar_bg']}; border-right: 1px solid {COLORS['border']};")
        self._active = ""
        self._buttons = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(4)

        # Logo
        logo = QLabel("⚡ APIForge")
        logo.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_lg']}px; font-weight: 700; padding: 8px 4px 16px 4px;")
        layout.addWidget(logo)

        # Divider
        layout.addWidget(self._divider())

        # QA Section
        qa_label = QLabel("QA ENGINEER")
        qa_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; font-weight: 600; padding: 12px 4px 4px 4px; letter-spacing: 1px;")
        layout.addWidget(qa_label)

        self._add_btn(layout, "home",         "🏠  Home",            "home")
        self._add_btn(layout, "qa_home",      "🧪  QA Dashboard",    "qa_home")
        self._add_btn(layout, "doc_input",    "📄  Import API",       "doc_input")
        self._add_btn(layout, "flow_screen",  "🔀  API Flow",         "flow_screen")
        self._add_btn(layout, "test_runner",  "▶️   Run Tests",        "test_runner")
        self._add_btn(layout, "evidence_screen","📋  Evidence",        "evidence_screen")
        self._add_btn(layout, "report_screen","📊  Reports",          "report_screen")

        # Divider
        layout.addWidget(self._divider())

        # Dev Section
        dev_label = QLabel("DEVELOPER")
        dev_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; font-weight: 600; padding: 12px 4px 4px 4px; letter-spacing: 1px;")
        layout.addWidget(dev_label)

        self._add_btn(layout, "dev_home",          "🏗️   Dev Dashboard",  "dev_home")
        self._add_btn(layout, "requirement_input", "📝  Requirements",    "requirement_input")
        self._add_btn(layout, "stack_screen",      "🛠️   Stack Advisor",   "stack_screen")
        self._add_btn(layout, "architecture_screen","🗺️   Architecture",   "architecture_screen")
        self._add_btn(layout, "export_screen",     "📤  Export",          "export_screen")

        layout.addStretch()

        # Version
        ver = QLabel("v0.1.0")
        ver.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; padding: 4px;")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ver)

    def _add_btn(self, layout, name: str, label: str, route: str):
        btn = QPushButton(label)
        btn.setObjectName("ghost")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color:            {COLORS['text_secondary']};
                border:           none;
                border-radius:    8px;
                padding:          10px 12px;
                text-align:       left;
                font-size:        {FONTS['size_sm']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_primary']};
            }}
        """)
        btn.clicked.connect(lambda _, r=route: self._on_click(r))
        self._buttons[name] = btn
        layout.addWidget(btn)

    def _on_click(self, route: str):
        self.set_active(route)
        self.navigate.emit(route)

    def set_active(self, name: str):
        if self._active and self._active in self._buttons:
            btn = self._buttons[self._active]
            btn.setStyleSheet(btn.styleSheet().replace(
                f"background-color: {COLORS['accent']};", "background-color: transparent;"
            ))
        self._active = name
        if name in self._buttons:
            self._buttons[name].setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color:            white;
                    border:           none;
                    border-radius:    8px;
                    padding:          10px 12px;
                    text-align:       left;
                    font-size:        {FONTS['size_sm']}px;
                }}
            """)

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        return line
