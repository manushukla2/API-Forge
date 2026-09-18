from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


CATEGORY_COLORS = {
    "happy_path": "#22c55e",
    "negative":   "#ef4444",
    "edge_case":  "#f59e0b",
    "security":   "#a855f7",
    "ai_specific":"#6366f1"
}


class ScenarioCard(QFrame):
    run_clicked = pyqtSignal(dict)

    def __init__(self, scenario: dict, parent=None):
        super().__init__(parent)
        self.scenario = scenario
        self.setObjectName("card")
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
            QFrame#card:hover {{
                border-color: {COLORS['accent']};
            }}
        """)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(12)

        # Left — ID + category
        left = QVBoxLayout()
        left.setSpacing(4)

        sc_id = QLabel(self.scenario.get("id", "TC000"))
        sc_id.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_xs']}px; font-weight: 700;")
        left.addWidget(sc_id)

        category = self.scenario.get("category", "")
        color    = CATEGORY_COLORS.get(category, COLORS["text_secondary"])
        cat_label = QLabel(category.replace("_", " ").title())
        cat_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border:           1px solid {color};
                border-radius:    4px;
                font-size:        {FONTS['size_xs']}px;
                padding:          2px 6px;
            }}
        """)
        left.addWidget(cat_label)
        layout.addLayout(left)

        # Middle — name
        mid = QVBoxLayout()
        mid.setSpacing(2)

        name = QLabel(self.scenario.get("name", ""))
        name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        name.setWordWrap(True)
        mid.addWidget(name)

        method = self.scenario.get("method", "")
        url    = self.scenario.get("url", "")
        if method or url:
            detail = QLabel(f"{method}  {url}")
            detail.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            mid.addWidget(detail)

        layout.addLayout(mid)
        layout.addStretch()

        # Right — run button
        run_btn = QPushButton("▶ Run")
        run_btn.setFixedWidth(70)
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color:            white;
                border:           none;
                border-radius:    6px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          6px 0px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
        """)
        run_btn.clicked.connect(lambda: self.run_clicked.emit(self.scenario))
        layout.addWidget(run_btn)
