from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS
from studio.component_library import ComponentLibrary


class ArchitectureScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lib     = ComponentLibrary()
        self._result = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        title = QLabel("🗺️ Architecture")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        sub = QLabel("Visual architecture based on your recommended stack")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.canvas = QWidget()
        self.canvas_layout = QVBoxLayout(self.canvas)
        self.canvas_layout.setSpacing(12)
        self.canvas_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.canvas)
        layout.addWidget(scroll)

    def load(self, result: dict):
        self._result = result
        while self.canvas_layout.count():
            item = self.canvas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stack      = result.get("stack", {}).get("recommended_stack", {})
        boilerplate = result.get("boilerplate", {})
        components  = self.lib.get_all()

        # Group by category
        categories = {}
        for key, comp in components.items():
            cat = comp["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((key, comp))

        cat_order = ["infrastructure", "api", "framework", "ai", "database", "cache", "auth", "deployment"]

        for cat in cat_order:
            if cat not in categories:
                continue

            cat_label = QLabel(cat.upper())
            cat_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; font-weight: 700; letter-spacing: 1px; padding: 8px 0 4px 0;")
            self.canvas_layout.addWidget(cat_label)

            row = QHBoxLayout()
            row.setSpacing(10)

            for key, comp in categories[cat]:
                is_selected = self._is_in_stack(key, stack)
                row.addWidget(self._comp_card(comp, is_selected))

            row.addStretch()

            row_widget = QWidget()
            row_widget.setLayout(row)
            self.canvas_layout.addWidget(row_widget)

        self.canvas_layout.addStretch()

    def _is_in_stack(self, key: str, stack: dict) -> bool:
        stack_values = [v.lower() for v in stack.values()]
        return any(key.replace("_", "").lower() in v.replace(" ", "").lower() for v in stack_values)

    def _comp_card(self, comp: dict, selected: bool) -> QFrame:
        color = COLORS["accent"] if selected else COLORS["border"]
        card  = QFrame()
        card.setFixedSize(130, 90)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           2px solid {color};
                border-radius:    10px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel(comp.get("icon", ""))
        icon.setStyleSheet("font-size: 20px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        name = QLabel(comp.get("name", ""))
        name.setStyleSheet(f"color: {'#fff' if selected else COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; font-weight: {'700' if selected else '400'};")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setWordWrap(True)
        layout.addWidget(name)

        return card
