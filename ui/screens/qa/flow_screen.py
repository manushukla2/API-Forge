from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS
from ui.components.flow_diagram import FlowDiagram


class FlowScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._flow_data = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("🔀 API Flow")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.endpoint_count = QLabel("0 endpoints")
        self.endpoint_count.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        header.addWidget(self.endpoint_count)
        layout.addLayout(header)

        # Meta row
        self.meta_row = QHBoxLayout()
        self.meta_row.setSpacing(16)
        layout.addLayout(self.meta_row)

        # Flow diagram
        self.diagram = FlowDiagram()
        layout.addWidget(self.diagram)

    def load(self, flow_data: dict):
        self._flow_data = flow_data
        nodes = flow_data.get("nodes", [])
        self.endpoint_count.setText(f"{len(nodes)} endpoints")

        # Clear meta row
        while self.meta_row.count():
            item = self.meta_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Meta badges
        auth = flow_data.get("auth_endpoint", None)
        if auth:
            self._add_badge(f"🔐 Auth: {auth}", COLORS["warning"])

        entries = flow_data.get("entry_points", [])
        if entries:
            self._add_badge(f"▶ Entry: {entries[0]}", COLORS["success"])

        exits = flow_data.get("exit_points", [])
        if exits:
            self._add_badge(f"⏹ Exit: {exits[0]}", COLORS["danger"])

        self.meta_row.addStretch()
        self.diagram.load(flow_data)

    def _add_badge(self, text: str, color: str):
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border:           1px solid {color};
                border-radius:    6px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          4px 10px;
            }}
        """)
        self.meta_row.addWidget(label)
