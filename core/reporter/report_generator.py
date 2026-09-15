import json
import datetime
from config.settings import REPORTS_DIR
from core.reporter.pdf_exporter import PDFExporter
from core.reporter.html_exporter import HTMLExporter
from core.reporter.json_exporter import JSONExporter
import os


class ReportGenerator:
    def __init__(self, session_id: str):
        self.session_id  = session_id
        self.report_dir  = os.path.join(REPORTS_DIR, session_id)
        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self, api_info: dict, evidence_list: list, format: str = "html") -> str:
        report_data = self._build_report_data(api_info, evidence_list)

        if format == "pdf":
            exporter = PDFExporter()
        elif format == "json":
            exporter = JSONExporter()
        else:
            exporter = HTMLExporter()

        output_path = os.path.join(self.report_dir, f"report.{format}")
        return exporter.export(report_data, output_path)

    def _build_report_data(self, api_info: dict, evidence_list: list) -> dict:
        total   = len(evidence_list)
        passed  = sum(1 for e in evidence_list if e["assertions"]["status"] == "passed")
        failed  = total - passed

        avg_latency = 0
        if evidence_list:
            avg_latency = round(
                sum(e["response"]["latency_ms"] for e in evidence_list) / total, 2
            )

        return {
            "meta": {
                "session_id":   self.session_id,
                "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "api_title":    api_info.get("title", "Unknown API"),
                "api_version":  api_info.get("version", "1.0.0"),
                "base_url":     api_info.get("base_url", "")
            },
            "summary": {
                "total":       total,
                "passed":      passed,
                "failed":      failed,
                "pass_rate":   round((passed / total * 100), 2) if total > 0 else 0,
                "avg_latency": avg_latency
            },
            "evidence": evidence_list
        }
