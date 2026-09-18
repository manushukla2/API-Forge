from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS


NODE_COLORS = {
    "entry":   "#22c55e",
    "exit":    "#ef4444",
    "auth":    "#f59e0b",
    "default": "#6366f1"
}


class FlowNode(QFrame):
    def __init__(self, node: dict, parent=None):
        super().__init__(parent)
        node_type = node.get("type", "default")
        color     = NODE_COLORS.get(node_type, NODE_COLORS["default"])

        self.setFixedWidth(220)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           2px solid {color};
                border-radius:    10px;
                padding:          8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Type badge
        badge = QLabel(node_type.upper())
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border-radius:    4px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      700;
                padding:          2px 6px;
            }}
        """)
        badge.setFixedWidth(70)
        layout.addWidget(badge)

        # Endpoint label
        label = QLabel(node.get("label", ""))
        label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xs']}px; font-weight: 600;")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Description
        desc = node.get("description", "")
        if desc:
            desc_label = QLabel(desc[:60] + "..." if len(desc) > 60 else desc)
            desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)


class FlowDiagram(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: {COLORS['bg_primary']}; border: none;")

        self.canvas = QWidget()
        self.canvas.setStyleSheet(f"background-color: {COLORS['bg_primary']};")
        self.canvas_layout = QVBoxLayout(self.canvas)
        self.canvas_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.canvas_layout.setSpacing(8)

        scroll.setWidget(self.canvas)
        layout.addWidget(scroll)

    def load(self, flow_data: dict):
        # Clear existing
        while self.canvas_layout.count():
            item = self.canvas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        nodes = flow_data.get("nodes", [])
        edges = flow_data.get("edges", [])

        if not nodes:
            empty = QLabel("No flow data available")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
            self.canvas_layout.addWidget(empty)
            return

        for i, node in enumerate(nodes):
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Step number
            step_label = QLabel(f"Step {i+1}")
            step_label.setFixedWidth(50)
            step_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            row.addWidget(step_label)

            # Node
            flow_node = FlowNode(node)
            row.addWidget(flow_node)

            # Arrow if not last
            if i < len(nodes) - 1:
                arrow = QLabel("↓")
                arrow.setStyleSheet(f"color: {COLORS['accent']}; font-size: 18px; padding: 4px;")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

            row_widget = QWidget()
            row_widget.setLayout(row)
            self.canvas_layout.addWidget(row_widget)

            # Arrow between nodes
            if i < len(nodes) - 1:
                arrow_widget = QLabel("     ↓")
                arrow_widget.setStyleSheet(f"color: {COLORS['accent']}; font-size: 16px;")
                self.canvas_layout.addWidget(arrow_widget)
