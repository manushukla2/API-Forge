from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
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
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header
        header = QHBoxLayout()
        title = QLabel("🧪 QA Dashboard")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        new_btn = QPushButton("+ New Test Session")
        new_btn.setFixedHeight(40)
        new_btn.clicked.connect(lambda: self.navigate.emit("doc_input"))
        header.addWidget(new_btn)
        layout.addLayout(header)

        # Stats row
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        layout.addLayout(self.stats_row)

        # Sessions list
        sessions_label = QLabel("Recent Sessions")
        sessions_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        layout.addWidget(sessions_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.sessions_widget = QWidget()
        self.sessions_layout = QVBoxLayout(self.sessions_widget)
        self.sessions_layout.setSpacing(8)
        self.sessions_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.sessions_widget)
        layout.addWidget(scroll)

        self.refresh()

    def refresh(self):
        # Clear
        while self.sessions_layout.count():
            item = self.sessions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sessions = self.session_manager.list_sessions()

        # Stats
        total  = len(sessions)
        passed = sum(1 for s in sessions if s.get("status") == "completed")

        for val, lbl in [(str(total), "Total Sessions"), (str(passed), "Completed"), ("HTML/JSON", "Export Formats")]:
            card = QFrame()
            card.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px;")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 14, 20, 14)
            v = QLabel(val)
            v.setStyleSheet(f"color: {COLORS['accent']}; font-size: {FONTS['size_2xl']}px; font-weight: 800;")
            l = QLabel(lbl)
            l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
            cl.addWidget(v)
            cl.addWidget(l)
            self.stats_row.addWidget(card)

        self.stats_row.addStretch()

        if not sessions:
            empty = QLabel("No sessions yet — start a new test session")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px; padding: 40px;")
            self.sessions_layout.addWidget(empty)
            return

        for s in sessions:
            self.sessions_layout.addWidget(self._session_card(s))

    def _session_card(self, session: dict) -> QFrame:
        card = QFrame()
        card.setFixedHeight(68)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
            QFrame:hover {{
                border-color: {COLORS['accent']};
            }}
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)

        info = QVBoxLayout()
        name = QLabel(session.get("api_title", "Unknown API"))
        name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        info.addWidget(name)

        meta = QLabel(f"{session.get('created_at', '')[:19]}  |  {session.get('total_endpoints', 0)} endpoints")
        meta.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        info.addWidget(meta)

        layout.addLayout(info)
        layout.addStretch()

        status = session.get("status", "")
        color  = COLORS["success"] if status == "completed" else COLORS["warning"]
        status_label = QLabel(status.upper())
        status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color:            {color};
                border:           1px solid {color};
                border-radius:    4px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          2px 8px;
            }}
        """)
        layout.addWidget(status_label)

        return card
