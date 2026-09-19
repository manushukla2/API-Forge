from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QFileDialog, QTabWidget)
from PyQt6.QtCore import Qt
from ui.theme import COLORS, FONTS
from ui.components.code_viewer import CodeViewer
from ui.components.json_viewer import JsonViewer
from ui.components.toast import Toast
import os


class ExportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("📤 Export")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        save_btn = QPushButton("💾 Save Project")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self._save_project)
        header.addWidget(save_btn)
        layout.addLayout(header)

        # Tabs
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

        # FastAPI code tab
        self.code_viewer = CodeViewer("python")
        tabs.addTab(self.code_viewer, "⚡ FastAPI Code")

        # Swagger spec tab
        self.swagger_viewer = JsonViewer()
        tabs.addTab(self.swagger_viewer, "📋 OpenAPI Spec")

        # Boilerplate tab
        self.boilerplate_viewer = JsonViewer()
        tabs.addTab(self.boilerplate_viewer, "🗂️ Boilerplate")

        layout.addWidget(tabs)

        # Export buttons
        export_frame = QFrame()
        export_frame.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px;")
        ef_layout = QHBoxLayout(export_frame)
        ef_layout.setContentsMargins(20, 14, 20, 14)
        ef_layout.setSpacing(12)

        for label, handler in [
            ("📄 Export FastAPI Code", self._export_code),
            ("📋 Export OpenAPI Spec", self._export_swagger),
            ("🗂️ Export Full Project",  self._save_project)
        ]:
            btn = QPushButton(label)
            btn.setFixedHeight(40)
            btn.clicked.connect(handler)
            ef_layout.addWidget(btn)

        ef_layout.addStretch()
        layout.addWidget(export_frame)

        self.toast = Toast(self)

    def load(self, result: dict):
        self._result = result
        fastapi_code = result.get("fastapi_code", "# No code generated")
        swagger_spec = result.get("swagger_spec", {})
        boilerplate  = result.get("boilerplate", {})

        self.code_viewer.set_code(fastapi_code)
        self.swagger_viewer.load(swagger_spec)
        self.boilerplate_viewer.load(boilerplate)

    def _export_code(self):
        code = self.code_viewer.get_code()
        if not code:
            self.toast.error("No code to export")
            return
        dest, _ = QFileDialog.getSaveFileName(self, "Save FastAPI Code", "main.py", "Python (*.py)")
        if dest:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(code)
            self.toast.success("FastAPI code exported!")

    def _export_swagger(self):
        import json
        spec = self._result.get("swagger_spec", {})
        if not spec:
            self.toast.error("No OpenAPI spec to export")
            return
        dest, _ = QFileDialog.getSaveFileName(self, "Save OpenAPI Spec", "openapi.json", "JSON (*.json)")
        if dest:
            with open(dest, "w", encoding="utf-8") as f:
                json.dump(spec, f, indent=2)
            self.toast.success("OpenAPI spec exported!")

    def _save_project(self):
        from core.developer.project_scaffolder import ProjectScaffolder
        boilerplate = self._result.get("boilerplate", {})
        if not boilerplate:
            self.toast.error("No project to save")
            return
        dest = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if dest:
            scaffolder = ProjectScaffolder()
            result     = scaffolder.scaffold(boilerplate, dest)
            self.toast.success(f"Project saved — {result['created_files']} files created!")
