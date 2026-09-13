import json
import yaml
import requests
from typing import Union


class SwaggerParser:
    def parse(self, source: str) -> dict:
        """
        source = file path ya URL
        Returns structured endpoints dict
        """
        raw = self._load(source)
        return self._extract(raw)

    def _load(self, source: str) -> dict:
        # URL se load karo
        if source.startswith("http://") or source.startswith("https://"):
            r = requests.get(source, timeout=15)
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return yaml.safe_load(r.text)

        # File se load karo
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            return json.loads(content)
        except Exception:
            return yaml.safe_load(content)

    def _extract(self, raw: dict) -> dict:
        endpoints = []
        base_url  = self._get_base_url(raw)
        paths     = raw.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() not in ["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"]:
                    continue

                endpoints.append({
                    "method":      method.upper(),
                    "path":        path,
                    "full_url":    f"{base_url}{path}",
                    "summary":     details.get("summary", ""),
                    "description": details.get("description", ""),
                    "tags":        details.get("tags", []),
                    "parameters":  details.get("parameters", []),
                    "request_body": details.get("requestBody", {}),
                    "responses":   details.get("responses", {}),
                    "security":    details.get("security", [])
                })

        return {
            "title":      raw.get("info", {}).get("title", "Unknown API"),
            "version":    raw.get("info", {}).get("version", "1.0.0"),
            "base_url":   base_url,
            "total":      len(endpoints),
            "endpoints":  endpoints
        }

    def _get_base_url(self, raw: dict) -> str:
        # OpenAPI 3.x
        servers = raw.get("servers", [])
        if servers:
            return servers[0].get("url", "").rstrip("/")

        # Swagger 2.x
        host    = raw.get("host", "localhost")
        schemes = raw.get("schemes", ["https"])
        base    = raw.get("basePath", "/")
        return f"{schemes[0]}://{host}{base}".rstrip("/")
