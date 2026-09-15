import json
import os
from core.ai.ai_router import get_ai_router


class ScenarioGenerator:
    def __init__(self):
        self.router  = get_ai_router()
        self.prompt  = self._load_prompt()

    def _load_prompt(self) -> str:
        path = os.path.join(
            os.path.dirname(__file__),
            "prompts", "scenario_generator.md"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def generate(self, endpoint: dict) -> dict:
        user_msg = f"""
Generate test scenarios for this API endpoint:

Method:      {endpoint.get('method', 'GET')}
URL:         {endpoint.get('full_url', endpoint.get('path', ''))}
Summary:     {endpoint.get('summary', '')}
Description: {endpoint.get('description', '')}
Parameters:  {json.dumps(endpoint.get('parameters', []), indent=2)}
Request Body:{json.dumps(endpoint.get('request_body', {}), indent=2)}
Responses:   {json.dumps(endpoint.get('responses', {}), indent=2)}
"""
        result = self.router.chat_json(self.prompt, user_msg)

        try:
            data = json.loads(result)
            # Ensure required fields
            if "scenarios" not in data:
                data["scenarios"] = []
            if "endpoint" not in data:
                data["endpoint"] = f"{endpoint.get('method')} {endpoint.get('path')}"
            return data
        except Exception:
            return {
                "endpoint":        f"{endpoint.get('method')} {endpoint.get('path')}",
                "total_scenarios": 0,
                "scenarios":       []
            }

    def generate_bulk(self, endpoints: list) -> list:
        results = []
        for endpoint in endpoints:
            result = self.generate(endpoint)
            results.append(result)
        return results
