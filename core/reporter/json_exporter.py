import json


class JSONExporter:
    def export(self, report_data: dict, output_path: str) -> str:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        return output_path
