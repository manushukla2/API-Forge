import requests
import time
from config.settings import DEFAULT_TIMEOUT, DEFAULT_RETRIES
from config.constants import HTTPMethod


class APIRunner:
    def __init__(self, base_url: str = "", headers: dict = {}):
        self.base_url       = base_url.rstrip("/")
        self.default_headers = headers
        self.session        = requests.Session()
        self.session.headers.update(headers)

    def run(self, endpoint: dict) -> dict:
        method   = endpoint.get("method", "GET").upper()
        url      = endpoint.get("full_url", "") or f"{self.base_url}{endpoint.get('path', '')}"
        headers  = {**self.default_headers, **endpoint.get("headers", {})}
        body     = endpoint.get("request_body", {})
        params   = endpoint.get("query_params", {})

        return self._execute(method, url, headers, body, params)

    def _execute(self, method: str, url: str, headers: dict, body: dict, params: dict) -> dict:
        attempt  = 0
        last_err = None

        while attempt < DEFAULT_RETRIES:
            try:
                start    = time.time()
                response = self.session.request(
                    method  = method,
                    url     = url,
                    headers = headers,
                    json    = body if body else None,
                    params  = params,
                    timeout = DEFAULT_TIMEOUT
                )
                elapsed = round((time.time() - start) * 1000, 2)

                return {
                    "success":     True,
                    "status_code": response.status_code,
                    "latency_ms":  elapsed,
                    "headers":     dict(response.headers),
                    "body":        self._parse_response(response),
                    "raw":         response.text[:5000],
                    "url":         url,
                    "method":      method,
                    "attempt":     attempt + 1
                }

            except requests.exceptions.Timeout:
                last_err = "Request timed out"
            except requests.exceptions.ConnectionError:
                last_err = "Connection failed"
            except Exception as e:
                last_err = str(e)

            attempt += 1
            time.sleep(1)

        return {
            "success":     False,
            "status_code": 0,
            "latency_ms":  0,
            "headers":     {},
            "body":        {},
            "raw":         "",
            "url":         url,
            "method":      method,
            "error":       last_err,
            "attempt":     attempt
        }

    def _parse_response(self, response) -> dict:
        try:
            return response.json()
        except Exception:
            return {"text": response.text[:2000]}
