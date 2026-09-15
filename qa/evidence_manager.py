import os
import json
from config.settings import SESSIONS_DIR


class EvidenceManager:
    def __init__(self, session_id: str):
        self.session_id  = session_id
        self.session_dir = os.path.join(SESSIONS_DIR, session_id)

    def get_all(self) -> list:
        evidence = []
        if not os.path.exists(self.session_dir):
            return evidence
        for fname in sorted(os.listdir(self.session_dir)):
            if fname.startswith("EV") and fname.endswith(".json"):
                path = os.path.join(self.session_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    evidence.append(json.load(f))
        return evidence

    def get_by_status(self, status: str) -> list:
        return [
            e for e in self.get_all()
            if e["assertions"]["status"] == status
        ]

    def get_by_id(self, evidence_id: str) -> dict:
        path = os.path.join(self.session_dir, f"{evidence_id}.json")
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_summary(self) -> dict:
        evidence  = self.get_all()
        total     = len(evidence)
        passed    = sum(1 for e in evidence if e["assertions"]["status"] == "passed")
        failed    = total - passed
        latencies = [e["response"]["latency_ms"] for e in evidence]

        return {
            "session_id":  self.session_id,
            "total":       total,
            "passed":      passed,
            "failed":      failed,
            "pass_rate":   round((passed / total * 100), 2) if total > 0 else 0,
            "avg_latency": round(sum(latencies) / total, 2) if total > 0 else 0,
            "max_latency": max(latencies) if latencies else 0,
            "min_latency": min(latencies) if latencies else 0
        }

    def tag_evidence(self, evidence_id: str, tag: str):
        evidence = self.get_by_id(evidence_id)
        if not evidence:
            return
        tags = evidence.get("tags", [])
        if tag not in tags:
            tags.append(tag)
        evidence["tags"] = tags
        path = os.path.join(self.session_dir, f"{evidence_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)

    def add_note(self, evidence_id: str, note: str):
        evidence = self.get_by_id(evidence_id)
        if not evidence:
            return
        evidence["note"] = note
        path = os.path.join(self.session_dir, f"{evidence_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)
