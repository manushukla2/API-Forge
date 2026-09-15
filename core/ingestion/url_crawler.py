import requests
from core.ai.ai_router import get_ai_router
import json


class URLCrawler:
    def crawl(self, url: str) -> dict:
        base_url = self._get_base_url(url)
        found    = {}

        # Step 1 — Common doc endpoints try karo
        found = self._try_doc_endpoints(base_url)
        if found:
            return found

        # Step 2 — Common API endpoints probe karo
        live_endpoints = self._probe_common_paths(base_url)

        # Step 3 — AI se structure infer karo
        return self._ai_infer(base_url, live_endpoints)

    def _get_base_url(self, url: str) -> str:
        from urllib.parse import urlparse
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}"

    def _try_doc_endpoints(self, base_url: str) -> dict:
        doc_paths = [
            "/openapi.json",
            "/swagger.json",
            "/api/docs",
            "/api/openapi.json",
            "/v1/openapi.json",
            "/docs/openapi.json"
        ]
        for path in doc_paths:
            try:
                r = requests.get(f"{base_url}{path}", timeout=5)
                if r.status_code == 200 and "openapi" in r.text.lower():
                    from core.ingestion.swagger_parser import SwaggerParser
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=".json",
                        delete=False, encoding="utf-8"
                    ) as f:
                        f.write(r.text)
                        tmp = f.name
                    result = SwaggerParser().parse(tmp)
                    os.unlink(tmp)
                    return result
            except Exception:
                continue
        return {}

    def _probe_common_paths(self, base_url: str) -> list:
        common = [
            "/health", "/api", "/api/v1", "/api/v2",
            "/users", "/auth", "/login", "/register",
            "/products", "/orders", "/items", "/search"
        ]
        live = []
        for path in common:
            try:
                r = requests.get(f"{base_url}{path}", timeout=3)
                live.append({
                    "path":   path,
                    "status": r.status_code,
                    "method": "GET"
                })
            except Exception:
                continue
        return live

    def _ai_infer(self, base_url: str, live_endpoints: list) -> dict:
        system_prompt = """
You are an API discovery expert.
Given a base URL and list of discovered live endpoints, infer the full API structure.
Return ONLY valid JSON in this format:
{
  "title": "Inferred API name",
  "version": "1.0.0",
  "base_url": "https://api.example.com",
  "total": 3,
  "endpoints": [
    {
      "method": "GET",
      "path": "/api/v1/users",
      "full_url": "https://api.example.com/api/v1/users",
      "summary": "Get all users",
      "description": "Inferred from discovery",
      "tags": [],
      "parameters": [],
      "request_body": {},
      "responses": {}
    }
  ]
}
"""
        user_msg = f"Base URL: {base_url}\nDiscovered endpoints: {json.dumps(live_endpoints)}"
        router   = get_ai_router()
        result   = router.chat_json(system_prompt, user_msg)

        try:
            return json.loads(result)
        except Exception:
            return {
                "title":     "Unknown API",
                "version":   "1.0.0",
                "base_url":  base_url,
                "total":     len(live_endpoints),
                "endpoints": live_endpoints
            }
