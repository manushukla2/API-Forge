import re
import json


class CurlParser:
    def parse(self, source: str) -> dict:
        endpoints = []
        endpoint  = self._parse_curl(source)
        if endpoint:
            endpoints.append(endpoint)

        return {
            "title":     "cURL Import",
            "version":   "1.0.0",
            "base_url":  self._extract_base_url(endpoint.get("full_url", "")),
            "total":     len(endpoints),
            "endpoints": endpoints
        }

    def _parse_curl(self, curl: str) -> dict:
        curl = curl.strip()

        # Method
        method_match = re.search(r"-X\s+([A-Z]+)", curl)
        method       = method_match.group(1) if method_match else "GET"

        # URL
        url_match = re.search(r"curl\s+(?:-X\s+\w+\s+)?['\"]?(https?://[^\s'\"]+)['\"]?", curl)
        url       = url_match.group(1) if url_match else ""

        # Headers
        headers = {}
        for h in re.findall(r"-H\s+['\"]([^'\"]+)['\"]", curl):
            if ":" in h:
                k, v     = h.split(":", 1)
                headers[k.strip()] = v.strip()

        # Body
        body = {}
        body_match = re.search(r"(?:-d|--data|--data-raw)\s+['\"](.+?)['\"](?:\s|$)", curl, re.DOTALL)
        if body_match:
            try:
                body = json.loads(body_match.group(1))
            except Exception:
                body = {"raw": body_match.group(1)}

        # Auth
        auth = {}
        auth_match = re.search(r"-u\s+['\"]?([^'\"\s]+)['\"]?", curl)
        if auth_match:
            auth = {"type": "basic", "value": auth_match.group(1)}

        bearer_match = re.search(r"Bearer\s+([^\s'\"]+)", curl)
        if bearer_match:
            auth = {"type": "bearer", "value": bearer_match.group(1)}

        return {
            "method":       method,
            "path":         self._extract_path(url),
            "full_url":     url,
            "summary":      f"{method} {self._extract_path(url)}",
            "description":  "Imported from cURL",
            "tags":         [],
            "parameters":   [],
            "request_body": body,
            "headers":      headers,
            "auth":         auth,
            "responses":    {}
        }

    def _extract_path(self, url: str) -> str:
        try:
            from urllib.parse import urlparse
            return urlparse(url).path or "/"
        except Exception:
            return "/"

    def _extract_base_url(self, url: str) -> str:
        try:
            from urllib.parse import urlparse
            p = urlparse(url)
            return f"{p.scheme}://{p.netloc}"
        except Exception:
            return ""
