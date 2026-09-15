from core.ai.scenario_generator import ScenarioGenerator


class TestSuiteBuilder:
    def __init__(self):
        self.generator = ScenarioGenerator()

    def build(self, api_data: dict) -> dict:
        endpoints = api_data.get("endpoints", [])
        suite     = {
            "api_title":   api_data.get("title", "Unknown API"),
            "base_url":    api_data.get("base_url", ""),
            "total_endpoints": len(endpoints),
            "total_scenarios": 0,
            "suites":          []
        }

        for endpoint in endpoints:
            scenario_data = self.generator.generate(endpoint)
            scenarios     = scenario_data.get("scenarios", [])

            suite["suites"].append({
                "endpoint":        f"{endpoint.get('method')} {endpoint.get('path')}",
                "summary":         endpoint.get("summary", ""),
                "total_scenarios": len(scenarios),
                "scenarios":       scenarios
            })
            suite["total_scenarios"] += len(scenarios)

        return suite

    def filter_by_category(self, suite: dict, category: str) -> dict:
        filtered = {**suite, "suites": []}
        for s in suite.get("suites", []):
            filtered_scenarios = [
                sc for sc in s.get("scenarios", [])
                if sc.get("category", "") == category
            ]
            if filtered_scenarios:
                filtered["suites"].append({
                    **s,
                    "scenarios":       filtered_scenarios,
                    "total_scenarios": len(filtered_scenarios)
                })
        filtered["total_scenarios"] = sum(
            len(s["scenarios"]) for s in filtered["suites"]
        )
        return filtered

    def get_categories(self, suite: dict) -> list:
        categories = set()
        for s in suite.get("suites", []):
            for sc in s.get("scenarios", []):
                cat = sc.get("category", "")
                if cat:
                    categories.add(cat)
        return sorted(list(categories))
