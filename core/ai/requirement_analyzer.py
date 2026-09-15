import json
import os
from core.ai.ai_router import get_ai_router


class RequirementAnalyzer:
    def __init__(self):
        self.router = get_ai_router()
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        path = os.path.join(
            os.path.dirname(__file__),
            "prompts", "requirement_analyzer.md"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def analyze(self, requirements: str) -> dict:
        truncated = requirements[:3000]
        result    = self.router.chat_json(
            self.prompt,
            f"Analyze these requirements:\n\n{truncated}"
        )

        try:
            data = json.loads(result)
            if "core_features" not in data:
                return self._fallback(requirements)
            return data
        except Exception:
            return self._fallback(requirements)

    def _fallback(self, requirements: str) -> dict:
        return {
            "project_name":    "Unknown Project",
            "summary":         requirements[:100],
            "core_features":   [],
            "suggested_endpoints": [],
            "data_entities":   [],
            "non_functional": {
                "expected_users": "unknown",
                "security_level": "standard",
                "performance":    "standard",
                "compliance":     []
            },
            "integrations":  [],
            "constraints": {
                "budget":           "unknown",
                "timeline":         "unknown",
                "tech_preferences": []
            }
        }
