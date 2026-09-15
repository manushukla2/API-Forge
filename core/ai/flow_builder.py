import json
import os
from core.ai.ai_router import get_ai_router


class FlowBuilder:
    def __init__(self):
        self.router = get_ai_router()
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        path = os.path.join(
            os.path.dirname(__file__),
            "prompts", "flow_builder.md"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def build(self, api_data: dict) -> dict:
        endpoints = api_data.get("endpoints", [])

        if not endpoints:
            return self._empty_flow()

        user_msg = f"""
Analyze these API endpoints and build a logical flow:

API Title:  {api_data.get('title', 'Unknown API')}
Base URL:   {api_data.get('base_url', '')}
Total:      {len(endpoints)}

Endpoints:
{json.dumps([
    {
        'method':      e.get('method'),
        'path':        e.get('path'),
        'summary':     e.get('summary', ''),
        'description': e.get('description', ''),
        'tags':        e.get('tags', [])
    }
    for e in endpoints
], indent=2)}
"""
        result = self.router.chat_json(self.prompt, user_msg)

        try:
            data = json.loads(result)
            if "flows" not in data:
                data["flows"] = []
            return data
        except Exception:
            return self._empty_flow()

    def _empty_flow(self) -> dict:
        return {
            "total_endpoints": 0,
            "entry_points":    [],
            "exit_points":     [],
            "auth_endpoint":   None,
            "flows":           [],
            "parallel_groups": [],
            "critical_path":   []
        }
