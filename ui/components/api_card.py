from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS


METHOD_COLORS = {
    "GET":    "#22c55e",
    "POST":   "#6366f1",
    "PUT":    "#f59e0b",
    "PATCH":  "#f97316",
    "DELETE": "#ef4444",
    "OPTIONS":"#94a3b8",
    "HEAD":   "#94a3b8"
}


class APICard(QFrame):
    def __init__(self, endpoint: dict, parent=None):
        super().__init__(parent)
        self.endpoint = endpoint
        self.setObjectName("card")
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
                padding:          12px;
            }}
            QFrame#card:hover {{
                border-color:     {COLORS['accent']};
            }}
        """)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Method badge
        method = self.endpoint.get("method", "GET")
        color  = METHOD_COLORS.get(method, COLORS["text_secondary"])

        method_label = QLabel(method)
        method_label.setFixedWidth(64)
        method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        method_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border:           1px solid {color};
                border-radius:    6px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      700;
                padding:          4px 0px;
            }}
        """)
        layout.addWidget(method_label)

        # Path + summary
        info = QVBoxLayout()
        info.setSpacing(2)

        path = QLabel(self.endpoint.get("path", ""))
        path.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        info.addWidget(path)

        summary = self.endpoint.get("summary", "")
        if summary:
            desc = QLabel(summary)
            desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            info.addWidget(desc)

        layout.addLayout(info)
        layout.addStretch()

        # Tags
        for tag in self.endpoint.get("tags", [])[:2]:
            tag_label = QLabel(tag)
            tag_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['bg_secondary']};
                    color:            {COLORS['text_secondary']};
                    border-radius:    4px;
                    font-size:        {FONTS['size_xs']}px;
                    padding:          2px 8px;
                }}
            """)
            layout.addWidget(tag_label)
