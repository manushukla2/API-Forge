from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QFrame, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS
from ui.components.json_viewer import JsonViewer


class EvidenceScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._evidence = []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("📋 Test Evidence")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.count_label = QLabel("0 items")
        self.count_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        header.addWidget(self.count_label)
        layout.addLayout(header)

        # Filter row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)

        for label, val in [("All", "all"), ("Passed ✅", "passed"), ("Failed ❌", "failed")]:
            btn = QPushButton(label)
            btn.setObjectName("ghost")
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda _, v=val: self._filter(v))
            filter_row.addWidget(btn)

        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Splitter — list + detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left — evidence list
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(6)

        scroll.setWidget(self.list_widget)
        left_layout.addWidget(scroll)
        splitter.addWidget(left)

        # Right — detail view
        right = QWidget()
        right.setStyleSheet(f"background-color: {COLORS['bg_secondary']}; border-radius: 10px;")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 16, 16, 16)

        detail_title = QLabel("Select an evidence item to inspect")
        detail_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        detail_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(detail_title)

        self.detail_view = JsonViewer()
        right_layout.addWidget(self.detail_view)

        splitter.addWidget(right)
        splitter.setSizes([400, 600])
        layout.addWidget(splitter)

    def load(self, evidence_list: list):
        self._evidence = evidence_list
        self._render(evidence_list)

    def _render(self, evidence_list: list):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.count_label.setText(f"{len(evidence_list)} items")

        for e in evidence_list:
            self.list_layout.addWidget(self._evidence_card(e))

    def _evidence_card(self, e: dict) -> QFrame:
        status = e["assertions"]["status"]
        color  = COLORS["success"] if status == "passed" else COLORS["danger"]
        icon   = "✅" if status == "passed" else "❌"

        card = QFrame()
        card.setFixedHeight(64)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-left:      3px solid {color};
                border-radius:    8px;
            }}
            QFrame:hover {{
                border-color:     {color};
            }}
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)

        left = QVBoxLayout()
        id_label = QLabel(f"{icon}  {e.get('id', '')}")
        id_label.setStyleSheet(f"color: {color}; font-size: {FONTS['size_xs']}px; font-weight: 700;")
        left.addWidget(id_label)

        method = e["endpoint"]["method"]
        url    = e["endpoint"]["url"]
        ep_label = QLabel(f"{method}  {url[:45]}{'...' if len(url) > 45 else ''}")
        ep_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xs']}px;")
        left.addWidget(ep_label)

        layout.addLayout(left)
        layout.addStretch()

        latency = QLabel(f"{e['response']['latency_ms']}ms")
        latency.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        layout.addWidget(latency)

        card.mousePressEvent = lambda event, ev=e: self.detail_view.load(ev)
        return card

    def _filter(self, status: str):
        if status == "all":
            self._render(self._evidence)
        else:
            filtered = [e for e in self._evidence if e["assertions"]["status"] == status]
            self._render(filtered)
