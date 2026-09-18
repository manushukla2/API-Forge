from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS
from ui.components.scenario_card import ScenarioCard


class ScenarioScreen(QWidget):
    run_scenario = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._suite = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("🧾 Test Scenarios")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.total_label = QLabel("0 scenarios")
        self.total_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        header.addWidget(self.total_label)
        layout.addLayout(header)

        # Filter row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)

        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        filter_row.addWidget(filter_label)

        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.setFixedHeight(36)
        self.category_filter.currentTextChanged.connect(self._on_filter)
        filter_row.addWidget(self.category_filter)

        self.endpoint_filter = QComboBox()
        self.endpoint_filter.addItem("All Endpoints")
        self.endpoint_filter.setFixedHeight(36)
        self.endpoint_filter.currentTextChanged.connect(self._on_filter)
        filter_row.addWidget(self.endpoint_filter)

        filter_row.addStretch()

        run_all_btn = QPushButton("▶ Run All")
        run_all_btn.setFixedHeight(36)
        run_all_btn.clicked.connect(self._run_all)
        filter_row.addWidget(run_all_btn)

        layout.addLayout(filter_row)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(8)

        scroll.setWidget(self.list_widget)
        layout.addWidget(scroll)

    def load(self, suite: dict):
        self._suite = suite
        self.total_label.setText(f"{suite.get('total_scenarios', 0)} scenarios")

        # Populate filters
        self.category_filter.clear()
        self.category_filter.addItem("All Categories")
        self.endpoint_filter.clear()
        self.endpoint_filter.addItem("All Endpoints")

        categories = set()
        for s in suite.get("suites", []):
            self.endpoint_filter.addItem(s.get("endpoint", ""))
            for sc in s.get("scenarios", []):
                cat = sc.get("category", "")
                if cat:
                    categories.add(cat)

        for cat in sorted(categories):
            self.category_filter.addItem(cat)

        self._render_all()

    def _render_all(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for suite in self._suite.get("suites", []):
            # Endpoint header
            ep_label = QLabel(suite.get("endpoint", ""))
            ep_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_sm']}px; font-weight: 700; padding: 8px 0 4px 0;")
            self.list_layout.addWidget(ep_label)

            for sc in suite.get("scenarios", []):
                card = ScenarioCard(sc)
                card.run_clicked.connect(self.run_scenario.emit)
                self.list_layout.addWidget(card)

    def _on_filter(self):
        cat = self.category_filter.currentText()
        ep  = self.endpoint_filter.currentText()

        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for suite in self._suite.get("suites", []):
            if ep != "All Endpoints" and suite.get("endpoint") != ep:
                continue

            scenarios = suite.get("scenarios", [])
            if cat != "All Categories":
                scenarios = [s for s in scenarios if s.get("category") == cat]

            if not scenarios:
                continue

            ep_label = QLabel(suite.get("endpoint", ""))
            ep_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_sm']}px; font-weight: 700; padding: 8px 0 4px 0;")
            self.list_layout.addWidget(ep_label)

            for sc in scenarios:
                card = ScenarioCard(sc)
                card.run_clicked.connect(self.run_scenario.emit)
                self.list_layout.addWidget(card)

    def _run_all(self):
        for suite in self._suite.get("suites", []):
            for sc in suite.get("scenarios", []):
                self.run_scenario.emit(sc)
