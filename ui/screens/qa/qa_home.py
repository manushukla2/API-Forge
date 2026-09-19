from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QScrollArea, QLineEdit,
                              QComboBox, QTableWidget, QTableWidgetItem,
                              QHeaderView, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from ui.theme import COLORS, FONTS
from core.tester.session_manager import SessionManager


class QAHomeScreen(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session_manager = SessionManager()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # ── Header ──────────────────────────────────────────
        header = QHBoxLayout()

        left_header = QVBoxLayout()
        left_header.setSpacing(2)
        title = QLabel("QA Dashboard")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 22px; font-weight: 700;")
        sub = QLabel("Monitor your API testing workspace.")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        left_header.addWidget(title)
        left_header.addWidget(sub)
        header.addLayout(left_header)
        header.addStretch()

        import_btn = QPushButton("  Import API")
        import_btn.setFixedHeight(38)
        import_btn.setFixedWidth(120)
        import_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
                font-size:        {FONTS['size_sm']}px;
                font-weight:      600;
                padding:          0 16px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_secondary']};
            }}
        """)
        import_btn.clicked.connect(lambda: self.navigate.emit("doc_input"))
        header.addWidget(import_btn)

        new_btn = QPushButton("+ New test session")
        new_btn.setFixedHeight(38)
        new_btn.setFixedWidth(160)
        new_btn.setStyleSheet(f"""
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
        new_btn.clicked.connect(lambda: self.navigate.emit("doc_input"))
        header.addWidget(new_btn)
        layout.addLayout(header)

        # ── Stats Cards ─────────────────────────────────────
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        layout.addLayout(self.stats_row)

        # ── Recent Sessions ─────────────────────────────────
        sessions_label = QLabel("Recent sessions")
        sessions_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_md']}px; font-weight: 700;")
        layout.addWidget(sessions_label)

        # Search + Filter row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search sessions...")
        self.search_box.setFixedHeight(36)
        self.search_box.setFixedWidth(280)
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
                padding:          0 12px;
                font-size:        {FONTS['size_sm']}px;
            }}
        """)
        self.search_box.textChanged.connect(self._on_search)
        filter_row.addWidget(self.search_box)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All statuses", "Completed", "Running", "Failed"])
        self.status_filter.setFixedHeight(36)
        self.status_filter.setFixedWidth(140)
        self.status_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
                border-radius:    8px;
                padding:          0 12px;
                font-size:        {FONTS['size_sm']}px;
            }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
            }}
        """)
        self.status_filter.currentTextChanged.connect(self._on_filter)
        filter_row.addWidget(self.status_filter)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # ── Table ───────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["API NAME", "LAST RUN", "ENDPOINTS", "STATUS", "ACTIONS"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
                font-size:        {FONTS['size_sm']}px;
                gridline-color:   transparent;
            }}
            QTableWidget::item {{
                padding:          12px 16px;
                border-bottom:    1px solid {COLORS['border']};
                color:            {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_card']};
                color:            {COLORS['text_secondary']};
                border:           none;
                border-bottom:    1px solid {COLORS['border']};
                padding:          10px 16px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                letter-spacing:   1px;
            }}
        """)
        layout.addWidget(self.table)

        # ── Pipeline Health ──────────────────────────────────
        health_frame = QFrame()
        health_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
            }}
        """)
        health_layout = QVBoxLayout(health_frame)
        health_layout.setContentsMargins(20, 16, 20, 16)
        health_layout.setSpacing(12)

        health_header = QHBoxLayout()
        health_title = QLabel("Pipeline health")
        health_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_md']}px; font-weight: 700;")
        health_header.addWidget(health_title)
        health_header.addStretch()
        self.health_pct = QLabel("0%")
        self.health_pct.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        health_header.addWidget(self.health_pct)
        overall_label = QLabel("Overall pipeline health")
        overall_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        health_header.addWidget(overall_label)
        health_layout.addLayout(health_header)

        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(0)
        self.health_bar.setTextVisible(False)
        self.health_bar.setFixedHeight(8)
        self.health_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['bg_secondary']};
                border:           none;
                border-radius:    4px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent']};
                border-radius:    4px;
            }}
        """)
        health_layout.addWidget(self.health_bar)

        stages_row = QHBoxLayout()
        for stage in ["Import", "Discover", "Test", "Evidence"]:
            lbl = QLabel(stage)
            lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            stages_row.addWidget(lbl)
            if stage != "Evidence":
                stages_row.addStretch()
        health_layout.addLayout(stages_row)
        layout.addWidget(health_frame)

        self.refresh()

    def refresh(self):
        sessions = self.session_manager.list_sessions()
        self._sessions = sessions
        self._render_stats(sessions)
        self._render_table(sessions)
        self._render_health(sessions)

    def _render_stats(self, sessions):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total     = len(sessions)
        completed = sum(1 for s in sessions if s.get("status") == "completed")
        rate      = round((completed / total * 100)) if total > 0 else 0

        stats = [
            ("Total sessions", str(total),    "+12%  this month", COLORS["accent"]),
            ("Completed",      str(completed), f"{rate}% completion rate", COLORS["success"]),
            ("Export formats", "3",            "HTML, JSON, PDF",  "#f59e0b"),
        ]

        for lbl, val, sub, color in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['bg_card']};
                    border:           1px solid {COLORS['border']};
                    border-radius:    12px;
                }}
            """)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(24, 20, 24, 20)
            cl.setSpacing(8)

            l = QLabel(lbl)
            l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
            cl.addWidget(l)

            v = QLabel(val)
            v.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 36px; font-weight: 800;")
            cl.addWidget(v)

            bar = QFrame()
            bar.setFixedHeight(4)
            bar.setFixedWidth(60)
            bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
            cl.addWidget(bar)

            s = QLabel(sub)
            s.setStyleSheet(f"color: {COLORS['success'] if 'month' in sub else COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            cl.addWidget(s)

            self.stats_row.addWidget(card)

    def _render_table(self, sessions):
        self.table.setRowCount(len(sessions))

        STATUS_COLORS = {
            "completed":  (COLORS["success"], "Passed"),
            "running":    ("#f59e0b",          "In progress"),
            "failed":     (COLORS["danger"],   "Failed"),
            "created":    (COLORS["text_secondary"], "Created"),
        }

        for row, s in enumerate(sessions):
            self.table.setRowHeight(row, 52)

            # API Name
            name_item = QTableWidgetItem(s.get("api_title", "Unknown API"))
            name_item.setForeground(QColor(COLORS["text_primary"]))
            self.table.setItem(row, 0, name_item)

            # Last run
            ts = s.get("created_at", "")[:16].replace("T", "  ")
            time_item = QTableWidgetItem(ts)
            time_item.setForeground(QColor(COLORS["text_secondary"]))
            self.table.setItem(row, 1, time_item)

            # Endpoints
            ep_item = QTableWidgetItem(str(s.get("total_endpoints", 0)))
            ep_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ep_item.setForeground(QColor(COLORS["text_primary"]))
            self.table.setItem(row, 2, ep_item)

            # Status badge
            status     = s.get("status", "created")
            color, lbl = STATUS_COLORS.get(status, (COLORS["text_secondary"], status.title()))
            status_item = QTableWidgetItem(f"● {lbl}")
            status_item.setForeground(QColor(color))
            self.table.setItem(row, 3, status_item)

            # Actions
            action_lbl = "View" if status == "completed" else "Open" if status == "running" else "Review"
            action_item = QTableWidgetItem(action_lbl)
            action_item.setForeground(QColor(COLORS["accent"]))
            action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, action_item)

    def _render_health(self, sessions):
        total     = len(sessions)
        completed = sum(1 for s in sessions if s.get("status") == "completed")
        health    = round((completed / total * 100)) if total > 0 else 0
        self.health_bar.setValue(health)
        self.health_pct.setText(f"{health}%")

    def _on_search(self, text: str):
        filtered = [s for s in self._sessions
                    if text.lower() in s.get("api_title", "").lower()]
        self._render_table(filtered)

    def _on_filter(self, status: str):
        if status == "All statuses":
            self._render_table(self._sessions)
        else:
            filtered = [s for s in self._sessions
                        if s.get("status", "").lower() == status.lower()]
            self._render_table(filtered)
