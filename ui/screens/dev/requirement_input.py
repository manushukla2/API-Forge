from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from ui.theme import COLORS, FONTS
from ui.components.progress_bar import ProgressWidget
from ui.components.toast import Toast


class StudioWorker(QThread):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(dict)
    error    = pyqtSignal(str)

    def __init__(self, requirements: str):
        super().__init__()
        self.requirements = requirements

    def run(self):
        try:
            from studio.studio_controller import StudioController
            controller = StudioController()
            result = controller.run_full_pipeline(
                requirements = self.requirements,
                on_progress  = lambda msg, val: self.progress.emit(msg, val)
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RequirementInputScreen(QWidget):
    studio_done = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("📝 Describe Your Requirements")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        sub = QLabel("Write your project requirements in plain language — any language, any detail level")
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        layout.addWidget(sub)

        # Examples
        examples_frame = QFrame()
        examples_frame.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px;")
        ex_layout = QVBoxLayout(examples_frame)
        ex_layout.setContentsMargins(16, 12, 16, 12)
        ex_layout.setSpacing(8)

        ex_title = QLabel("💡 Example prompts:")
        ex_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px; font-weight: 600;")
        ex_layout.addWidget(ex_title)

        examples = [
            "Build a REST API for a banking app with user auth, account management and transaction history",
            "I need a RAG chatbot API that answers questions from PDF documents using LangChain",
            "Create a multi-tenant SaaS API with JWT auth, subscription plans and usage analytics"
        ]

        for ex in examples:
            btn = QPushButton(f"› {ex}")
            btn.setObjectName("ghost")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color:            {COLORS['text_secondary']};
                    border:           none;
                    text-align:       left;
                    font-size:        {FONTS['size_xs']}px;
                    padding:          4px 0px;
                }}
                QPushButton:hover {{
                    color: {COLORS['accent']};
                }}
            """)
            btn.clicked.connect(lambda _, e=ex: self.input_box.setPlainText(e))
            ex_layout.addWidget(btn)

        layout.addWidget(examples_frame)

        # Input
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Describe what you want to build...")
        self.input_box.setMinimumHeight(180)
        self.input_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                color:            {COLORS['text_primary']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
                padding:          14px;
                font-size:        {FONTS['size_sm']}px;
            }}
            QTextEdit:focus {{
                border-color: {COLORS['accent']};
            }}
        """)
        layout.addWidget(self.input_box)

        # Progress
        self.progress = ProgressWidget()
        self.progress.hide()
        layout.addWidget(self.progress)

        layout.addStretch()

        # Analyze button
        self.analyze_btn = QPushButton("🚀 Analyze & Generate")
        self.analyze_btn.setFixedHeight(48)
        self.analyze_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color:            white;
                border:           none;
                border-radius:    10px;
                font-size:        {FONTS['size_md']}px;
                font-weight:      700;
            }}
            QPushButton:hover {{ background-color: #16a34a; }}
            QPushButton:disabled {{ background-color: {COLORS['border']}; }}
        """)
        self.analyze_btn.clicked.connect(self._start)
        layout.addWidget(self.analyze_btn)

        self.toast = Toast(self)

    def _start(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self.toast.error("Please describe your requirements")
            return

        self.analyze_btn.setEnabled(False)
        self.progress.show()
        self.progress.reset()

        self.worker = StudioWorker(text)
        self.worker.progress.connect(lambda msg, val: self.progress.update(msg, val))
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(lambda e: self.toast.error(e[:60]))
        self.worker.start()

    def _on_done(self, result: dict):
        self.analyze_btn.setEnabled(True)
        self.toast.success("Analysis complete!")
        self.studio_done.emit(result)
