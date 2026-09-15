import fitz
from core.ai.ai_router import get_ai_router
import json


class PDFParser:
    def parse(self, source: str) -> dict:
        text = self._extract_text(source)
        return self._ai_extract(text)

    def _extract_text(self, filepath: str) -> str:
        doc   = fitz.open(filepath)
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        return "\n".join(pages)

    def _ai_extract(self, text: str) -> dict:
        system_prompt = """
You are an expert API documentation analyzer.
Extract all API endpoints from the given documentation text.
Return ONLY valid JSON in this exact format:
{
  "title": "API name",
  "version": "version if found",
  "base_url": "base URL if found",
  "total": 3,
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/v1/login",
      "full_url": "https://api.example.com/api/v1/login",
      "summary": "User login",
      "description": "Authenticate user",
      "tags": [],
      "parameters": [],
      "request_body": {},
      "responses": {}
    }
  ]
}
"""
        # Truncate text to avoid token limits
        truncated = text[:3000]

        router = get_ai_router()
        result = router.chat_json(system_prompt, f"Extract endpoints from this documentation:\n\n{truncated}")

        try:
            return json.loads(result)
        except Exception:
            return {
                "title":     "Unknown API",
                "version":   "1.0.0",
                "base_url":  "",
                "total":     0,
                "endpoints": [],
                "raw_text":  text[:500]
            }
