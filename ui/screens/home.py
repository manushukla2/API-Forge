from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


class HomeScreen(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(32)
        layout.setContentsMargins(48, 48, 48, 48)

        # Hero
        hero = QVBoxLayout()
        hero.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.setSpacing(8)

        badge = QLabel("⚡ APIForge v0.1.0")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['accent']}22;
                color:            {COLORS['accent']};
                border:           1px solid {COLORS['accent']};
                border-radius:    99px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          4px 16px;
            }}
        """)
        badge.setFixedWidth(160)
        hero.addWidget(badge, alignment=Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Test & Build AI APIs")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 32px; font-weight: 800;")
        hero.addWidget(title)

        sub = QLabel("Drop your API docs — get a full test suite with evidence.\nOr describe your idea — get architecture, stack, and boilerplate.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_md']}px; line-height: 1.6;")
        sub.setWordWrap(True)
        hero.addWidget(sub)

        layout.addLayout(hero)

        # Cards row
        cards = QHBoxLayout()
        cards.setSpacing(20)

        cards.addWidget(self._card(
            "🧪", "QA Engineer",
            "Import API docs, generate test scenarios, run tests and export evidence reports.",
            "qa_home", COLORS["accent"]
        ))
        cards.addWidget(self._card(
            "🏗️", "Developer Studio",
            "Describe your requirements, get stack recommendations and boilerplate code.",
            "dev_home", "#22c55e"
        ))

        layout.addLayout(cards)

        # Stats row
        stats = QHBoxLayout()
        stats.setSpacing(16)
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for val, lbl in [("7", "Input Types"), ("5", "AI Agents"), ("3", "Export Formats"), ("∞", "Test Scenarios")]:
            stats.addWidget(self._stat(val, lbl))

        layout.addLayout(stats)

    def _card(self, icon, title, desc, route, color) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(340, 220)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    16px;
            }}
            QFrame:hover {{
                border-color: {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 32px;")
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_lg']}px; font-weight: 700;")
        layout.addWidget(title_label)

        desc_label = QLabel(desc)
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()

        btn = QPushButton(f"Open {title} →")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color:            white;
                border:           none;
                border-radius:    8px;
                padding:          8px 16px;
                font-size:        {FONTS['size_sm']}px;
                font-weight:      600;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        btn.clicked.connect(lambda _, r=route: self.navigate.emit(r))
        layout.addWidget(btn)

        return card

    def _stat(self, value, label) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setSpacing(2)

        val = QLabel(value)
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_2xl']}px; font-weight: 800;")
        l.addWidget(val)

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        l.addWidget(lbl)

        return w
