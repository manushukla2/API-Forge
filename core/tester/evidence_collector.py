import os
import json
import datetime
from config.settings import SESSIONS_DIR


class EvidenceCollector:
    def __init__(self, session_id: str):
        self.session_id  = session_id
        self.session_dir = os.path.join(SESSIONS_DIR, session_id)
        self.evidence    = []
        os.makedirs(self.session_dir, exist_ok=True)

    def collect(self, endpoint: dict, response: dict, assertion_result: dict) -> dict:
        timestamp = datetime.datetime.now().isoformat()

        evidence = {
            "id":          f"EV{len(self.evidence) + 1:03d}",
            "timestamp":   timestamp,
            "endpoint": {
                "method":  endpoint.get("method", ""),
                "url":     endpoint.get("full_url", ""),
                "headers": endpoint.get("headers", {}),
                "body":    endpoint.get("request_body", {})
            },
            "response": {
                "status_code": response.get("status_code", 0),
                "latency_ms":  response.get("latency_ms", 0),
                "headers":     response.get("headers", {}),
                "body":        response.get("body", {}),
                "raw":         response.get("raw", "")[:2000]
            },
            "assertions": {
                "status":  assertion_result.get("status", ""),
                "passed":  assertion_result.get("passed", 0),
                "failed":  assertion_result.get("failed", 0),
                "results": assertion_result.get("results", [])
            }
        }

        self.evidence.append(evidence)
        self._save_evidence(evidence)
        return evidence

    def _save_evidence(self, evidence: dict):
        filepath = os.path.join(self.session_dir, f"{evidence['id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)

    def save_session(self) -> str:
        summary = {
            "session_id":    self.session_id,
            "total":         len(self.evidence),
            "passed":        sum(1 for e in self.evidence if e["assertions"]["status"] == "passed"),
            "failed":        sum(1 for e in self.evidence if e["assertions"]["status"] == "failed"),
            "created_at":    datetime.datetime.now().isoformat(),
            "evidence_ids":  [e["id"] for e in self.evidence]
        }

        summary_path = os.path.join(self.session_dir, "session_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        return summary_path

    def get_all(self) -> list:
        return self.evidence

    def get_summary(self) -> dict:
        return {
            "session_id": self.session_id,
            "total":      len(self.evidence),
            "passed":     sum(1 for e in self.evidence if e["assertions"]["status"] == "passed"),
            "failed":     sum(1 for e in self.evidence if e["assertions"]["status"] == "failed")
        }
