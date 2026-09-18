from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS


class CodeViewer(QWidget):
    def __init__(self, language: str = "python", parent=None):
        super().__init__(parent)
        self.language = language
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(12, 8, 12, 8)

        lang_label = QPushButton(self.language.upper())
        lang_label.setEnabled(False)
        lang_label.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                color:            {COLORS['text_secondary']};
                border:           none;
                border-radius:    4px;
                font-size:        {FONTS['size_xs']}px;
                font-weight:      600;
                padding:          2px 8px;
            }}
        """)
        header.addWidget(lang_label)
        header.addStretch()

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("ghost")
        self.copy_btn.setFixedWidth(60)
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color:            {COLORS['text_secondary']};
                border:           1px solid {COLORS['border']};
                border-radius:    4px;
                font-size:        {FONTS['size_xs']}px;
                padding:          2px 8px;
            }}
            QPushButton:hover {{
                color:            {COLORS['text_primary']};
            }}
        """)
        self.copy_btn.clicked.connect(self._copy)
        header.addWidget(self.copy_btn)

        header_widget = QWidget()
        header_widget.setStyleSheet(f"background-color: {COLORS['bg_secondary']}; border-radius: 8px 8px 0 0;")
        header_widget.setLayout(header)
        layout.addWidget(header_widget)

        # Code area
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['bg_input']};
                color:            #e2e8f0;
                border:           1px solid {COLORS['border']};
                border-top:       none;
                border-radius:    0 0 8px 8px;
                padding:          12px;
            }}
        """)
        layout.addWidget(self.editor)

    def set_code(self, code: str):
        self.editor.setPlainText(code)

    def get_code(self) -> str:
        return self.editor.toPlainText()

    def _copy(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.editor.toPlainText())
        self.copy_btn.setText("✓")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy"))
