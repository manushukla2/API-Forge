from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QLinearGradient, QPalette, QColor, QPainter, QBrush
from ui.theme import COLORS, FONTS


class GradientFrame(QFrame):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor(124, 58, 237, 50))
        gradient.setColorAt(0.5, QColor(29, 78, 216, 35))
        gradient.setColorAt(1.0, QColor(24, 24, 27, 255))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QColor(COLORS["border"]))
        painter.drawRoundedRect(self.rect(), 16, 16)


class HomeScreen(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        # ── Header ───────────────────────────────────────────
        header = QHBoxLayout()

        left = QVBoxLayout()
        left.setSpacing(6)
        title = QLabel("Good morning")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;")
        sub = QLabel("Choose a workspace to get started.")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        left.addWidget(title)
        left.addWidget(sub)
        header.addLayout(left)
        header.addStretch()

        version_badge = QLabel("v0.1.0")
        version_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_secondary']};
                border:           1px solid {COLORS['border']};
                border-radius:    99px;
                font-size:        {FONTS['size_xs']}px;
                padding:          4px 12px;
            }}
        """)
        header.addWidget(version_badge)
        layout.addLayout(header)

        # ── Hero Section ─────────────────────────────────────
        hero = GradientFrame()
        hero.setMinimumHeight(280)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(32, 32, 32, 32)
        hero_layout.setSpacing(24)

        hero_text = QVBoxLayout()
        hero_text.setSpacing(10)

        tag = QLabel("API QUALITY + GENERATION")
        tag.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_xs']}px; font-weight: 700; letter-spacing: 3px;")
        hero_text.addWidget(tag)

        headline = QLabel("Build better APIs.\nTest with confidence.")
        headline.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 32px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2;")
        hero_text.addWidget(headline)

        desc = QLabel("From raw documentation to production-ready contracts and evidence.")
        desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_md']}px;")
        hero_text.addWidget(desc)
        hero_layout.addLayout(hero_text)

        # Cards row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(20)
        cards_row.addWidget(self._workspace_card(
            "⚗", "QA Engineer",
            "Discover, test, and prove every endpoint.",
            "Open QA workspace →", "qa_home"
        ))
        cards_row.addWidget(self._workspace_card(
            "</>", "Developer Studio",
            "Turn requirements into a complete API foundation.",
            "Open Developer Studio →", "dev_home"
        ))
        hero_layout.addLayout(cards_row)
        layout.addWidget(hero)

        # ── Stats Row ────────────────────────────────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        for val, lbl in [("7", "Input Types"), ("5", "AI Agents"), ("3", "Export Formats"), ("∞", "Test Scenarios")]:
            stats_row.addWidget(self._stat_card(val, lbl))
        layout.addLayout(stats_row)

        # ── Recent Activity ──────────────────────────────────
        activity_frame = QFrame()
        activity_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
            }}
        """)
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(24, 20, 24, 20)
        activity_layout.setSpacing(0)

        act_title = QLabel("Recent activity")
        act_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_md']}px; font-weight: 700; padding-bottom: 12px;")
        activity_layout.addWidget(act_title)

        activities = [
            ("▶", "Petstore API test run",  "2 min ago",  "Passed",    COLORS["success"]),
            ("✦", "RAG service scaffold",   "1 hour ago", "Generated", COLORS["accent"]),
            ("↑", "Payments API import",    "Yesterday",  "Ready",     COLORS["text_secondary"]),
        ]

        for i, (icon, name, time, badge, color) in enumerate(activities):
            row = QHBoxLayout()
            row.setContentsMargins(0, 14, 0, 14)
            row.setSpacing(14)

            icon_frame = QFrame()
            icon_frame.setFixedSize(36, 36)
            icon_frame.setStyleSheet(f"background-color: {COLORS['accent']}22; border-radius: 8px;")
            icon_layout = QVBoxLayout(icon_frame)
            icon_layout.setContentsMargins(0, 0, 0, 0)
            icon_lbl = QLabel(icon)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setStyleSheet(f"color: {COLORS['accent']}; font-size: 14px;")
            icon_layout.addWidget(icon_lbl)
            row.addWidget(icon_frame)

            text = QVBoxLayout()
            text.setSpacing(2)
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
            time_lbl = QLabel(time)
            time_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            text.addWidget(name_lbl)
            text.addWidget(time_lbl)
            row.addLayout(text)
            row.addStretch()

            badge_lbl = QLabel(badge)
            badge_lbl.setStyleSheet(f"""
                QLabel {{
                    background-color: {color}22;
                    color:            {color};
                    border-radius:    6px;
                    font-size:        {FONTS['size_xs']}px;
                    font-weight:      600;
                    padding:          3px 10px;
                }}
            """)
            row.addWidget(badge_lbl)

            row_widget = QWidget()
            row_widget.setLayout(row)
            if i < len(activities) - 1:
                row_widget.setStyleSheet(f"border-bottom: 1px solid {COLORS['border']};")
            activity_layout.addWidget(row_widget)

        layout.addWidget(activity_frame)
        layout.addStretch()

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _workspace_card(self, icon, title, desc, btn_text, route) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(30, 41, 59, 0.8);
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        top_row = QHBoxLayout()
        icon_frame = QFrame()
        icon_frame.setFixedSize(48, 48)
        icon_frame.setStyleSheet(f"background-color: {COLORS['accent']}22; border-radius: 12px;")
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"color: {COLORS['accent']}; font-size: 18px; font-weight: 700;")
        icon_layout.addWidget(icon_lbl)
        top_row.addWidget(icon_frame)
        top_row.addStretch()
        arrow = QLabel("↗")
        arrow.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 16px;")
        top_row.addWidget(arrow)
        layout.addLayout(top_row)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)

        layout.addStretch()

        btn = QPushButton(btn_text)
        btn.setFixedHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color:            white;
                border:           none;
                border-radius:    8px;
                font-size:        {FONTS['size_sm']}px;
                font-weight:      600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
        """)
        btn.clicked.connect(lambda _, r=route: self.navigate.emit(r))
        layout.addWidget(btn)
        return card

    def _stat_card(self, val, lbl) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(6)

        v = QLabel(val)
        v.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: 700;")
        layout.addWidget(v)

        l = QLabel(lbl)
        l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(l)
        return card
