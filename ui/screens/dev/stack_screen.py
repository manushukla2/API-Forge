from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea)
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS


class StackScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("🛠️ Stack Recommendation")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(16)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.content)
        layout.addWidget(scroll)

    def load(self, result: dict):
        self._result = result
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stack   = result.get("stack", {})
        reasons = stack.get("reasons", {})
        rec     = stack.get("recommended_stack", {})

        # Summary card
        summary = QFrame()
        summary.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['accent']}; border-radius: 12px;")
        sl = QVBoxLayout(summary)
        sl.setContentsMargins(20, 16, 20, 16)
        sl.setSpacing(8)

        sl.addWidget(self._label("✅ Recommended Stack", COLORS["accent"], FONTS["size_md"], bold=True))

        row = QHBoxLayout()
        row.setSpacing(10)
        for key, val in rec.items():
            badge = QFrame()
            badge.setStyleSheet(f"background-color: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px;")
            bl = QVBoxLayout(badge)
            bl.setContentsMargins(12, 8, 12, 8)
            bl.addWidget(self._label(key.replace("_", " ").upper(), COLORS["text_secondary"], FONTS["size_xs"]))
            bl.addWidget(self._label(val, COLORS["text_primary"], FONTS["size_sm"], bold=True))
            row.addWidget(badge)
        row.addStretch()
        sl.addLayout(row)
        self.content_layout.addWidget(summary)

        # Reasons
        if reasons:
            self.content_layout.addWidget(self._label("Why this stack?", COLORS["text_secondary"], FONTS["size_sm"], bold=True))
            for key, reason in reasons.items():
                card = QFrame()
                card.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 8px;")
                cl = QHBoxLayout(card)
                cl.setContentsMargins(14, 10, 14, 10)
                cl.addWidget(self._label(key.replace("_"," ").title() + ":", COLORS["accent"], FONTS["size_xs"], bold=True))
                cl.addWidget(self._label(reason, COLORS["text_secondary"], FONTS["size_xs"]))
                cl.addStretch()
                self.content_layout.addWidget(card)

        # Timeline
        timeline = stack.get("estimated_timeline", "")
        complexity = stack.get("estimated_complexity", "")
        if timeline or complexity:
            meta = QHBoxLayout()
            if complexity:
                meta.addWidget(self._badge(f"Complexity: {complexity}", COLORS["warning"]))
            if timeline:
                meta.addWidget(self._badge(f"Timeline: {timeline}", COLORS["success"]))
            meta.addStretch()
            self.content_layout.addLayout(meta)

        self.content_layout.addStretch()

    def _label(self, text, color, size, bold=False) -> QLabel:
        l = QLabel(text)
        weight = "700" if bold else "400"
        l.setStyleSheet(f"color: {color}; font-size: {size}px; font-weight: {weight};")
        l.setWordWrap(True)
        return l

    def _badge(self, text, color) -> QLabel:
        l = QLabel(text)
        l.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border:           1px solid {color};
                border-radius:    6px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          4px 12px;
            }}
        """)
        return l
