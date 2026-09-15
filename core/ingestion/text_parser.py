import json
from core.ai.ai_router import get_ai_router


class TextParser:
    def parse(self, source: str) -> dict:
        return self._ai_extract(source)

    def _ai_extract(self, text: str) -> dict:
        system_prompt = """
You are an expert API analyst.
Given a plain text description of an API or system, extract or infer all possible API endpoints.
If the text describes features or requirements (not endpoints directly), infer what endpoints would be needed.
Return ONLY valid JSON in this exact format:
{
  "title": "Inferred API name",
  "version": "1.0.0",
  "base_url": "",
  "total": 3,
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/v1/login",
      "full_url": "",
      "summary": "User login",
      "description": "Inferred from text",
      "tags": [],
      "parameters": [],
      "request_body": {
        "email": "string",
        "password": "string"
      },
      "responses": {
        "200": "Success",
        "401": "Unauthorized"
      }
    }
  ]
}
"""
        truncated = text[:2000]
        router    = get_ai_router()
        result    = router.chat_json(system_prompt, f"Extract API endpoints from this text:\n\n{truncated}")

        try:
            return json.loads(result)
        except Exception:
            return {
                "title":     "Unknown API",
                "version":   "1.0.0",
                "base_url":  "",
                "total":     0,
                "endpoints": [],
                "raw_text":  text[:300]
            }
