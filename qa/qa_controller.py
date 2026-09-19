import uuid
from core.ingestion.ingestion_router import route_input
from core.ai.scenario_generator import ScenarioGenerator
from core.ai.flow_builder import FlowBuilder
from core.tester.api_runner import APIRunner
from core.tester.auth_handler import AuthHandler
from core.tester.assertion_engine import AssertionEngine
from core.tester.evidence_collector import EvidenceCollector
from core.tester.session_manager import SessionManager
from core.reporter.report_generator import ReportGenerator


class QAController:
    def __init__(self):
        self.session_manager  = SessionManager()
        self.scenario_gen     = ScenarioGenerator()
        self.flow_builder     = FlowBuilder()
        self.assertion_engine = AssertionEngine()

    def run_full_pipeline(self, source: str, auth_config: dict = None, on_progress: callable = None) -> dict:
        auth_config = auth_config or {"type": "none"}

        self._emit(on_progress, "Parsing input...", 10)
        parsed   = route_input(source)
        api_data = parsed["data"]

        session_id = self.session_manager.create_session(api_data)
        self.session_manager.update_status(session_id, "running")
        collector  = EvidenceCollector(session_id)

        self._emit(on_progress, "Building API flow...", 20)
        flow = self.flow_builder.build(api_data)

        auth   = AuthHandler(auth_config)
        runner = APIRunner(
            base_url = api_data.get("base_url", ""),
            headers  = auth.get_headers()
        )

        endpoints = api_data.get("endpoints", [])
        total     = len(endpoints)

        for i, endpoint in enumerate(endpoints):
            if not isinstance(endpoint, dict):
                continue

            progress = 20 + int((i / total) * 60) if total > 0 else 80
            self._emit(on_progress, f"Testing {endpoint.get('method','GET')} {endpoint.get('path','')}...", progress)

            scenario_data = self.scenario_gen.generate(endpoint)
            scenarios     = scenario_data.get("scenarios", [])

            if not scenarios:
                scenarios = [{"assertions": []}]

            for scenario in scenarios:
                if not isinstance(scenario, dict):
                    continue

                ep_with_data = {**endpoint}
                if scenario.get("body") and isinstance(scenario.get("body"), dict):
                    ep_with_data["request_body"] = scenario["body"]
                if scenario.get("headers") and isinstance(scenario.get("headers"), dict):
                    ep_with_data["headers"] = {**endpoint.get("headers", {}), **scenario["headers"]}

                response = runner.run(ep_with_data)

                # Assertions — sirf dicts accept karo, strings skip karo
                raw_assertions = scenario.get("assertions", [])
                clean_assertions = []
                for a in raw_assertions:
                    if isinstance(a, dict):
                        clean_assertions.append(a)

                # Default assertions hamesha add karo
                clean_assertions.append({"type": "status_in",        "expected": [200, 201, 204]})
                clean_assertions.append({"type": "response_not_empty"})
                clean_assertions.append({"type": "latency_under",     "max_ms": 5000})

                result = self.assertion_engine.run(response, clean_assertions)
                collector.collect(endpoint, response, result)

        self._emit(on_progress, "Saving session...", 85)
        self.session_manager.update_status(session_id, "completed")
        collector.save_session()

        self._emit(on_progress, "Generating report...", 95)
        reporter  = ReportGenerator(session_id)
        html_path = reporter.generate(api_data, collector.get_all(), "html")
        json_path = reporter.generate(api_data, collector.get_all(), "json")

        self._emit(on_progress, "Done!", 100)

        return {
            "session_id": session_id,
            "api_info":   api_data,
            "flow":       flow,
            "summary":    collector.get_summary(),
            "evidence":   collector.get_all(),
            "reports": {
                "html": html_path,
                "json": json_path
            }
        }

    def _emit(self, callback, message: str, progress: int):
        if callback:
            callback(message, progress)
