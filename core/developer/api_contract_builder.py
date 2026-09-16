import json
from core.ai.ai_router import get_ai_router


class APIContractBuilder:
    def __init__(self):
        self.router = get_ai_router()

    def build(self, req_data: dict) -> dict:
        endpoints = req_data.get("suggested_endpoints", [])

        if not endpoints:
            return self._empty_contract(req_data)

        system_prompt = """
You are an API contract design expert.
Given a list of suggested endpoints, create a detailed API contract.
Return ONLY valid JSON in this format:
{
  "contract_version": "1.0.0",
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/v1/login",
      "summary": "User login",
      "request": {
        "headers": {"Content-Type": "application/json"},
        "body": {
          "email": {"type": "string", "required": true, "example": "user@example.com"},
          "password": {"type": "string", "required": true, "example": "password123"}
        }
      },
      "responses": {
        "200": {
          "description": "Success",
          "body": {
            "access_token": {"type": "string"},
            "token_type":   {"type": "string"}
          }
        },
        "401": {"description": "Invalid credentials", "body": {}}
      }
    }
  ]
}
"""
        user_msg = f"""
Build a detailed API contract for these endpoints:

Project: {req_data.get('project_name', 'Unknown')}
Summary: {req_data.get('summary', '')}

Endpoints:
{json.dumps(endpoints[:8], indent=2)}
"""
        result = self.router.chat_json(system_prompt, user_msg)

        try:
            data = json.loads(result)
            if "endpoints" not in data:
                return self._empty_contract(req_data)
            return data
        except Exception:
            return self._empty_contract(req_data)

    def _empty_contract(self, req_data: dict) -> dict:
        return {
            "contract_version": "1.0.0",
            "project":          req_data.get("project_name", "Unknown"),
            "endpoints":        []
        }
