import json
import os
from core.ai.ai_router import get_ai_router


class StackRecommender:
    def __init__(self):
        self.router = get_ai_router()
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        path = os.path.join(
            os.path.dirname(__file__),
            "prompts", "stack_recommender.md"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def recommend(self, requirements: str) -> dict:
        result = self.router.chat_json(self.prompt, f"Analyze these requirements and recommend a stack:\n\n{requirements}")

        try:
            data = json.loads(result)
            if "recommended_stack" not in data:
                return self._fallback()
            return data
        except Exception:
            return self._fallback()

    def _fallback(self) -> dict:
        return {
            "recommended_stack": {
                "api_framework": "FastAPI",
                "database":      "PostgreSQL",
                "ai_layer":      "LangChain",
                "deployment":    "Docker",
                "auth":          "JWT",
                "cache":         "Redis"
            },
            "reasons": {},
            "alternatives": [],
            "estimated_complexity": "medium",
            "estimated_timeline":   "4-6 weeks"
        }
