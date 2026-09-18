from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS
from studio.stack_profiles import StackProfiles


class DevHomeScreen(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profiles = StackProfiles()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header
        header = QHBoxLayout()
        title = QLabel("🏗️ Developer Studio")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        new_btn = QPushButton("+ New Project")
        new_btn.setFixedHeight(40)
        new_btn.clicked.connect(lambda: self.navigate.emit("requirement_input"))
        header.addWidget(new_btn)
        layout.addLayout(header)

        sub = QLabel("Describe your requirements — get stack recommendations, architecture, and boilerplate code")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        # Quick start
        quick_label = QLabel("Quick Start Templates")
        quick_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        layout.addWidget(quick_label)

        # Stack profile cards
        scroll_widget = QWidget()
        grid = QVBoxLayout(scroll_widget)
        grid.setSpacing(10)

        profiles = self.profiles.get_all()
        for key, profile in profiles.items():
            grid.addWidget(self._profile_card(key, profile))

        grid.addStretch()
        layout.addWidget(scroll_widget)

    def _profile_card(self, key: str, profile: dict) -> QFrame:
        card = QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
            QFrame:hover {{
                border-color: {COLORS['accent']};
            }}
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(16)

        info = QVBoxLayout()
        info.setSpacing(4)

        name = QLabel(profile.get("name", ""))
        name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 700;")
        info.addWidget(name)

        use_case = QLabel(profile.get("use_case", ""))
        use_case.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        info.addWidget(use_case)

        layout.addLayout(info)
        layout.addStretch()

        # Component badges
        for comp in profile.get("components", [])[:4]:
            badge = QLabel(comp.replace("_", " ").title())
            badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['bg_secondary']};
                    color:            {COLORS['text_secondary']};
                    border-radius:    4px;
                    font-size:        {FONTS['size_xs']}px;
                    padding:          2px 8px;
                }}
            """)
            layout.addWidget(badge)

        use_btn = QPushButton("Use →")
        use_btn.setFixedWidth(70)
        use_btn.setFixedHeight(32)
        use_btn.clicked.connect(lambda _, k=key: self.navigate.emit("requirement_input"))
        layout.addWidget(use_btn)

        return card
