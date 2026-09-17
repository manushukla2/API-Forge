from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme import COLORS, FONTS


class FileDropzone(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self, accepted: list = None, parent=None):
        super().__init__(parent)
        self.accepted = accepted or [".json", ".yaml", ".yml", ".pdf"]
        self.setAcceptDrops(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.zone = QLabel()
        self.zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zone.setMinimumHeight(140)
        self._set_idle()

        layout.addWidget(self.zone)

        btn = QPushButton("Browse File")
        btn.setObjectName("ghost")
        btn.setFixedWidth(120)
        btn.clicked.connect(self._browse)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _set_idle(self):
        exts = ", ".join(self.accepted)
        self.zone.setText(f"🗂️\n\nDrag & drop file here\n{exts}")
        self.zone.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_input']};
                border:           2px dashed {COLORS['border']};
                border-radius:    12px;
                color:            {COLORS['text_secondary']};
                font-size:        {FONTS['size_sm']}px;
                padding:          24px;
            }}
        """)

    def _set_active(self, filename: str):
        self.zone.setText(f"✅\n\n{filename}")
        self.zone.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_input']};
                border:           2px solid {COLORS['success']};
                border-radius:    12px;
                color:            {COLORS['success']};
                font-size:        {FONTS['size_sm']}px;
                padding:          24px;
            }}
        """)

    def _browse(self):
        exts = " ".join([f"*{e}" for e in self.accepted])
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", f"Files ({exts})")
        if path:
            self._set_active(path.split("/")[-1])
            self.file_selected.emit(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.zone.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['bg_secondary']};
                    border:           2px dashed {COLORS['accent']};
                    border-radius:    12px;
                    color:            {COLORS['accent']};
                    font-size:        {FONTS['size_sm']}px;
                    padding:          24px;
                }}
            """)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self._set_active(path.split("/")[-1])
            self.file_selected.emit(path)

    def dragLeaveEvent(self, event):
        self._set_idle()
