import json
import re
from config.constants import TestStatus


class AssertionEngine:
    def run(self, response: dict, assertions: list) -> dict:
        results = []
        passed  = 0
        failed  = 0

        for assertion in assertions:
            result = self._check(response, assertion)
            results.append(result)
            if result["passed"]:
                passed += 1
            else:
                failed += 1

        # Default assertions — hamesha chalein
        default_results = self._default_assertions(response)
        for r in default_results:
            results.append(r)
            if r["passed"]:
                passed += 1
            else:
                failed += 1

        overall = TestStatus.PASSED.value if failed == 0 else TestStatus.FAILED.value

        return {
            "status":  overall,
            "passed":  passed,
            "failed":  failed,
            "total":   len(results),
            "results": results
        }

    def _check(self, response: dict, assertion: dict) -> dict:
        a_type  = assertion.get("type", "")
        passed  = False
        message = ""

        try:
            if a_type == "status_code":
                expected = assertion.get("expected")
                actual   = response.get("status_code")
                passed   = actual == expected
                message  = f"Status code: expected {expected}, got {actual}"

            elif a_type == "status_in":
                expected = assertion.get("expected", [])
                actual   = response.get("status_code")
                passed   = actual in expected
                message  = f"Status {actual} in {expected}: {passed}"

            elif a_type == "response_contains":
                key      = assertion.get("key", "")
                expected = assertion.get("expected", "")
                raw      = response.get("raw", "")
                passed   = expected in raw
                message  = f"Response contains '{expected}': {passed}"

            elif a_type == "json_key_exists":
                key    = assertion.get("key", "")
                body   = response.get("body", {})
                passed = self._key_exists(body, key)
                message = f"JSON key '{key}' exists: {passed}"

            elif a_type == "json_value_equals":
                key      = assertion.get("key", "")
                expected = assertion.get("expected")
                body     = response.get("body", {})
                actual   = self._get_nested(body, key)
                passed   = actual == expected
                message  = f"JSON '{key}': expected {expected}, got {actual}"

            elif a_type == "latency_under":
                max_ms  = assertion.get("max_ms", 5000)
                actual  = response.get("latency_ms", 0)
                passed  = actual < max_ms
                message = f"Latency {actual}ms < {max_ms}ms: {passed}"

            elif a_type == "response_not_empty":
                raw    = response.get("raw", "")
                passed = len(raw.strip()) > 0
                message = f"Response not empty: {passed}"

            else:
                message = f"Unknown assertion type: {a_type}"

        except Exception as e:
            message = f"Assertion error: {str(e)}"

        return {
            "type":    a_type,
            "passed":  passed,
            "message": message
        }

    def _default_assertions(self, response: dict) -> list:
        results = []

        # Connection check
        results.append({
            "type":    "connection",
            "passed":  response.get("success", False),
            "message": "API reachable" if response.get("success") else f"Connection failed: {response.get('error', '')}"
        })

        # Not 5xx
        status = response.get("status_code", 0)
        results.append({
            "type":    "no_server_error",
            "passed":  status < 500 if status > 0 else False,
            "message": f"No server error (5xx): status={status}"
        })

        return results

    def _key_exists(self, obj, key: str) -> bool:
        keys = key.split(".")
        for k in keys:
            if isinstance(obj, dict) and k in obj:
                obj = obj[k]
            else:
                return False
        return True

    def _get_nested(self, obj, key: str):
        keys = key.split(".")
        for k in keys:
            if isinstance(obj, dict):
                obj = obj.get(k)
            else:
                return None
        return obj
