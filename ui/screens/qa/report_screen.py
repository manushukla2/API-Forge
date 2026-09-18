from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from ui.theme import COLORS, FONTS
from ui.components.toast import Toast
import os


class ReportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header
        title = QLabel("📊 Test Report")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_xl']}px; font-weight: 700;")
        layout.addWidget(title)

        # Summary cards
        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(16)
        self._total   = self._stat_card("0", "Total Tests",  COLORS["text_secondary"])
        self._passed  = self._stat_card("0", "Passed",       COLORS["success"])
        self._failed  = self._stat_card("0", "Failed",       COLORS["danger"])
        self._rate    = self._stat_card("0%","Pass Rate",    COLORS["accent"])
        self._latency = self._stat_card("0ms","Avg Latency", COLORS["accent"])
        self.cards_row.addStretch()
        layout.addLayout(self.cards_row)

        # Export section
        export_frame = QFrame()
        export_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    12px;
            }}
        """)
        export_layout = QVBoxLayout(export_frame)
        export_layout.setContentsMargins(24, 20, 24, 20)
        export_layout.setSpacing(16)

        export_title = QLabel("📤 Export Report")
        export_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['size_md']}px; font-weight: 700;")
        export_layout.addWidget(export_title)

        export_desc = QLabel("Download your test evidence report in your preferred format")
        export_desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_sm']}px;")
        export_layout.addWidget(export_desc)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.html_btn = QPushButton("🌐 Open HTML Report")
        self.html_btn.setFixedHeight(44)
        self.html_btn.clicked.connect(self._open_html)
        btn_row.addWidget(self.html_btn)

        self.json_btn = QPushButton("{ } Export JSON")
        self.json_btn.setFixedHeight(44)
        self.json_btn.setObjectName("ghost")
        self.json_btn.clicked.connect(self._export_json)
        btn_row.addWidget(self.json_btn)

        self.pdf_btn = QPushButton("📄 Export PDF")
        self.pdf_btn.setFixedHeight(44)
        self.pdf_btn.setObjectName("ghost")
        self.pdf_btn.clicked.connect(self._export_pdf)
        btn_row.addWidget(self.pdf_btn)

        btn_row.addStretch()
        export_layout.addLayout(btn_row)
        layout.addWidget(export_frame)

        layout.addStretch()

        # Toast
        self.toast = Toast(self)

    def _stat_card(self, val, lbl, color) -> QLabel:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border:           1px solid {COLORS['border']};
                border-radius:    10px;
            }}
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(24, 16, 24, 16)

        v = QLabel(val)
        v.setStyleSheet(f"color: {color}; font-size: {FONTS['size_2xl']}px; font-weight: 800;")
        cl.addWidget(v)

        l = QLabel(lbl)
        l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['size_xs']}px;")
        cl.addWidget(l)

        self.cards_row.insertWidget(self.cards_row.count() - 1, card)
        return v

    def load(self, result: dict):
        self._result = result
        summary = result.get("summary", {})
        self._total.setText(str(summary.get("total", 0)))
        self._passed.setText(str(summary.get("passed", 0)))
        self._failed.setText(str(summary.get("failed", 0)))

        total  = summary.get("total", 0)
        passed = summary.get("passed", 0)
        rate   = round((passed / total * 100), 1) if total > 0 else 0
        self._rate.setText(f"{rate}%")

    def _open_html(self):
        html = self._result.get("reports", {}).get("html", "")
        if html and os.path.exists(html):
            QDesktopServices.openUrl(QUrl.fromLocalFile(html))
        else:
            self.toast.error("HTML report not found")

    def _export_json(self):
        json_path = self._result.get("reports", {}).get("json", "")
        if not json_path or not os.path.exists(json_path):
            self.toast.error("JSON report not found")
            return
        dest, _ = QFileDialog.getSaveFileName(self, "Save JSON Report", "report.json", "JSON (*.json)")
        if dest:
            import shutil
            shutil.copy(json_path, dest)
            self.toast.success("JSON exported!")

    def _export_pdf(self):
        try:
            from core.reporter.pdf_exporter import PDFExporter
            from core.reporter.report_generator import ReportGenerator
            session_id = self._result.get("session_id", "")
            api_info   = self._result.get("api_info", {})
            evidence   = self._result.get("evidence", [])

            dest, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", "report.pdf", "PDF (*.pdf)")
            if dest:
                rg = ReportGenerator(session_id)
                rg.generate(api_info, evidence, "pdf")
                import shutil
                import os
                from config.settings import REPORTS_DIR
                pdf_src = os.path.join(REPORTS_DIR, session_id, "report.pdf")
                shutil.copy(pdf_src, dest)
                self.toast.success("PDF exported!")
        except Exception as e:
            self.toast.error(f"PDF export failed: {str(e)[:50]}")
