from core.ai.flow_builder import FlowBuilder


class FlowVisualizer:
    def __init__(self):
        self.builder = FlowBuilder()

    def build(self, api_data: dict) -> dict:
        flow = self.builder.build(api_data)
        return self._enrich(flow, api_data)

    def _enrich(self, flow: dict, api_data: dict) -> dict:
        nodes = []
        edges = []

        flows = flow.get("flows", [])

        for f in flows:
            endpoint = f.get("endpoint", "")
            step     = f.get("step", 0)
            nodes.append({
                "id":          str(step),
                "label":       endpoint,
                "description": f.get("description", ""),
                "parallel":    f.get("can_parallel", False),
                "type":        self._get_node_type(endpoint, flow)
            })

        for f in flows:
            step     = f.get("step", 0)
            outputs  = f.get("outputs_to", [])
            for target_endpoint in outputs:
                target_step = self._find_step(flows, target_endpoint)
                if target_step:
                    edges.append({
                        "from":      str(step),
                        "to":        str(target_step),
                        "data":      f.get("data_passed", []),
                        "label":     ", ".join(f.get("data_passed", []))
                    })

        return {
            "nodes":          nodes,
            "edges":          edges,
            "entry_points":   flow.get("entry_points", []),
            "exit_points":    flow.get("exit_points", []),
            "auth_endpoint":  flow.get("auth_endpoint", None),
            "critical_path":  flow.get("critical_path", []),
            "parallel_groups":flow.get("parallel_groups", []),
            "raw_flow":       flow
        }

    def _get_node_type(self, endpoint: str, flow: dict) -> str:
        auth = flow.get("auth_endpoint", "")
        if auth and auth in endpoint:
            return "auth"
        if endpoint in flow.get("entry_points", []):
            return "entry"
        if endpoint in flow.get("exit_points", []):
            return "exit"
        return "default"

    def _find_step(self, flows: list, endpoint: str) -> int:
        for f in flows:
            if f.get("endpoint", "") == endpoint:
                return f.get("step", 0)
        return None
