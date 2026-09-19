from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea, QTabWidget)
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS
from ui.components.json_viewer import JsonViewer
from ui.components.code_viewer import CodeViewer


class SchemaScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        title = QLabel("🗄️ Data Schema")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        sub = QLabel("Data entities and API contract generated from your requirements")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(sub)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {COLORS['bg_secondary']};
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color:            {COLORS['text_secondary']};
                padding:          8px 20px;
                border:           none;
            }}
            QTabBar::tab:selected {{
                color:        {COLORS['text_primary']};
                border-bottom: 2px solid {COLORS['accent']};
            }}
        """)

        # Entities tab
        self.entities_widget = QWidget()
        self.entities_layout = QVBoxLayout(self.entities_widget)
        self.entities_layout.setSpacing(10)
        self.entities_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        tabs.addTab(self.entities_widget, "📦 Data Entities")

        # Contract tab
        self.contract_viewer = JsonViewer()
        tabs.addTab(self.contract_viewer, "📋 API Contract")

        # Env vars tab
        self.env_viewer = CodeViewer("bash")
        tabs.addTab(self.env_viewer, "⚙️ Env Variables")

        layout.addWidget(tabs)

    def load(self, result: dict):
        self._result = result
        req         = result.get("requirements", {})
        contract    = result.get("contract", {})
        boilerplate = result.get("boilerplate", {})

        # Clear entities
        while self.entities_layout.count():
            item = self.entities_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Render entities
        entities = req.get("data_entities", [])
        if not entities:
            empty = QLabel("No data entities found")
            empty.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 20px;")
            self.entities_layout.addWidget(empty)
        else:
            for entity in entities:
                self.entities_layout.addWidget(self._entity_card(entity))

        self.entities_layout.addStretch()

        # Contract
        self.contract_viewer.load(contract)

        # Env vars
        env_vars = boilerplate.get("env_variables", [])
        env_text = "# Environment Variables\n\n"
        for var in env_vars:
            req_tag   = "# Required" if var.get("required") else "# Optional"
            env_text += f"{req_tag}\n{var.get('key', '')}={var.get('example', '')}\n\n"
        self.env_viewer.set_code(env_text)

    def _entity_card(self, entity: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Entity name
        name = QLabel(f"📦 {entity.get('name', '')}")
        name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 700;")
        layout.addWidget(name)

        # Fields
        fields_row = QHBoxLayout()
        fields_row.setSpacing(6)
        for field in entity.get("fields", []):
            badge = QLabel(field)
            badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['bg_secondary']};
                    color:            {COLORS['text_secondary']};
                    border:           1px solid {COLORS['border']};
                    border-radius:    4px;
                    font-size:        {FONTS['size_xs']}px;
                    padding:          2px 8px;
                }}
            """)
            fields_row.addWidget(badge)
        fields_row.addStretch()
        layout.addLayout(fields_row)

        # Relationships
        rels = entity.get("relationships", [])
        if rels:
            rel_label = QLabel(f"→ {', '.join(rels)}")
            rel_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_xs']}px;")
            layout.addWidget(rel_label)

        return card
