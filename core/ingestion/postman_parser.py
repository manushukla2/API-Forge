import json


class PostmanParser:
    def parse(self, source: str) -> dict:
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)

        endpoints = []
        collection_name = data.get("info", {}).get("name", "Unknown Collection")

        self._extract_items(data.get("item", []), endpoints)

        return {
            "title":     collection_name,
            "version":   "1.0.0",
            "base_url":  "",
            "total":     len(endpoints),
            "endpoints": endpoints
        }

    def _extract_items(self, items: list, endpoints: list, folder: str = ""):
        for item in items:
            # Folder ke andar items
            if "item" in item:
                folder_name = item.get("name", "")
                self._extract_items(item["item"], endpoints, folder_name)
                continue

            # Actual request
            request = item.get("request", {})
            if not request:
                continue

            method = request.get("method", "GET").upper()
            url    = self._extract_url(request.get("url", {}))
            headers = self._extract_headers(request.get("header", []))
            body    = self._extract_body(request.get("body", {}))

            endpoints.append({
                "method":       method,
                "path":         url,
                "full_url":     url,
                "summary":      item.get("name", ""),
                "description":  request.get("description", ""),
                "tags":         [folder] if folder else [],
                "parameters":   [],
                "request_body": body,
                "headers":      headers,
                "responses":    {}
            })

    def _extract_url(self, url_obj) -> str:
        if isinstance(url_obj, str):
            return url_obj
        if isinstance(url_obj, dict):
            raw = url_obj.get("raw", "")
            if raw:
                return raw
            # Reconstruct from parts
            host     = ".".join(url_obj.get("host", []))
            path     = "/".join(url_obj.get("path", []))
            protocol = url_obj.get("protocol", "https")
            return f"{protocol}://{host}/{path}"
        return ""

    def _extract_headers(self, headers: list) -> dict:
        return {h["key"]: h["value"] for h in headers if "key" in h}

    def _extract_body(self, body: dict) -> dict:
        if not body:
            return {}
        mode = body.get("mode", "")
        if mode == "raw":
            try:
                return json.loads(body.get("raw", "{}"))
            except Exception:
                return {"raw": body.get("raw", "")}
        elif mode == "formdata":
            return {f["key"]: f.get("value", "") for f in body.get("formdata", [])}
        elif mode == "urlencoded":
            return {f["key"]: f.get("value", "") for f in body.get("urlencoded", [])}
        return {}
