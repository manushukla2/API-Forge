import os
import json
import datetime
import uuid
from config.settings import SESSIONS_DIR


class SessionManager:
    def create_session(self, api_info: dict) -> str:
        session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        session_dir = os.path.join(SESSIONS_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)

        meta = {
            "session_id":  session_id,
            "created_at":  datetime.datetime.now().isoformat(),
            "api_title":   api_info.get("title", "Unknown API"),
            "api_version": api_info.get("version", "1.0.0"),
            "base_url":    api_info.get("base_url", ""),
            "total_endpoints": api_info.get("total", 0),
            "status":      "created"
        }

        self._save_meta(session_id, meta)
        return session_id

    def update_status(self, session_id: str, status: str):
        meta = self.load_meta(session_id)
        if meta:
            meta["status"]     = status
            meta["updated_at"] = datetime.datetime.now().isoformat()
            self._save_meta(session_id, meta)

    def load_meta(self, session_id: str) -> dict:
        path = os.path.join(SESSIONS_DIR, session_id, "meta.json")
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_sessions(self) -> list:
        sessions = []
        if not os.path.exists(SESSIONS_DIR):
            return sessions
        for name in sorted(os.listdir(SESSIONS_DIR), reverse=True):
            meta_path = os.path.join(SESSIONS_DIR, name, "meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    sessions.append(json.load(f))
        return sessions

    def load_evidence(self, session_id: str) -> list:
        session_dir = os.path.join(SESSIONS_DIR, session_id)
        evidence    = []
        if not os.path.exists(session_dir):
            return evidence
        for fname in sorted(os.listdir(session_dir)):
            if fname.startswith("EV") and fname.endswith(".json"):
                with open(os.path.join(session_dir, fname), "r", encoding="utf-8") as f:
                    evidence.append(json.load(f))
        return evidence

    def delete_session(self, session_id: str):
        import shutil
        session_dir = os.path.join(SESSIONS_DIR, session_id)
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)

    def _save_meta(self, session_id: str, meta: dict):
        path = os.path.join(SESSIONS_DIR, session_id, "meta.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
