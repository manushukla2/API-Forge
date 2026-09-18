from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from ui.theme import COLORS, FONTS
from ui.components.progress_bar import ProgressWidget
from ui.components.toast import Toast


class TestWorker(QThread):
    progress  = pyqtSignal(str, int)
    finished  = pyqtSignal(dict)
    error     = pyqtSignal(str)

    def __init__(self, source: str, auth_config: dict):
        super().__init__()
        self.source      = source
        self.auth_config = auth_config

    def run(self):
        try:
            from qa.qa_controller import QAController
            controller = QAController()
            result = controller.run_full_pipeline(
                source      = self.source,
                auth_config = self.auth_config,
                on_progress = lambda msg, val: self.progress.emit(msg, val)
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class TestRunnerScreen(QWidget):
    testing_done = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source      = ""
        self._auth_config = {}
        self._result      = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("▶️ Test Runner")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.run_btn = QPushButton("▶ Run All Tests")
        self.run_btn.setFixedHeight(40)
        self.run_btn.clicked.connect(self._start)
        header.addWidget(self.run_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setFixedHeight(40)
        self.stop_btn.setObjectName("danger")
        self.stop_btn.hide()
        header.addWidget(self.stop_btn)

        layout.addLayout(header)

        # Progress
        self.progress = ProgressWidget()
        layout.addWidget(self.progress)

        # Status cards
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        self._total_label   = self._stat_card("0", "Total",  COLORS["text_secondary"])
        self._passed_label  = self._stat_card("0", "Passed", COLORS["success"])
        self._failed_label  = self._stat_card("0", "Failed", COLORS["danger"])
        self._latency_label = self._stat_card("0ms","Avg Latency", COLORS["accent"])
        layout.addLayout(self.stats_row)

        # Log area
        log_label = QLabel("Test Log")
        log_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px; font-weight: 600;")
        layout.addWidget(log_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.log_widget  = QWidget()
        self.log_layout  = QVBoxLayout(self.log_widget)
        self.log_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log_layout.setSpacing(4)

        scroll.setWidget(self.log_widget)
        layout.addWidget(scroll)

        # Toast
        self.toast = Toast(self)

    def _stat_card(self, val, lbl, color) -> QLabel:
        card = QFrame()
        card.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px;")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 12, 20, 12)

        v = QLabel(val)
        v.setStyleSheet(f"color: {color}; font-size: {FONTS['size_2xl']}px; font-weight: 800;")
        cl.addWidget(v)

        l = QLabel(lbl)
        l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        cl.addWidget(l)

        self.stats_row.addWidget(card)
        return v

    def set_source(self, source: str, auth_config: dict):
        self._source      = source
        self._auth_config = auth_config

    def _start(self):
        if not self._source:
            self.toast.error("No source provided")
            return

        self.run_btn.setEnabled(False)
        self.stop_btn.show()
        self.progress.reset()
        self._clear_log()

        self.worker = TestWorker(self._source, self._auth_config)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    @pyqtSlot(str, int)
    def _on_progress(self, msg: str, val: int):
        self.progress.update(msg, val)
        self._add_log(msg, "info")

    @pyqtSlot(dict)
    def _on_done(self, result: dict):
        self._result = result
        summary = result.get("summary", {})
        self._total_label.setText(str(summary.get("total", 0)))
        self._passed_label.setText(str(summary.get("passed", 0)))
        self._failed_label.setText(str(summary.get("failed", 0)))
        self.run_btn.setEnabled(True)
        self.stop_btn.hide()
        self.toast.success("Testing complete!")
        self.testing_done.emit(result)

    @pyqtSlot(str)
    def _on_error(self, msg: str):
        self._add_log(f"Error: {msg}", "error")
        self.run_btn.setEnabled(True)
        self.stop_btn.hide()
        self.toast.error(f"Error: {msg[:60]}")

    def _add_log(self, msg: str, type: str = "info"):
        colors = {
            "info":    COLORS["text_secondary"],
            "success": COLORS["success"],
            "error":   COLORS["danger"]
        }
        label = QLabel(f"› {msg}")
        label.setStyleSheet(f"color: {colors.get(type, COLORS['text_secondary'])}; font-size: {FONTS['size_xs']}px;")
        self.log_layout.addWidget(label)

    def _clear_log(self):
        while self.log_layout.count():
            item = self.log_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
