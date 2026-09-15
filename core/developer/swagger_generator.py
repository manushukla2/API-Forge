import json
import os
from core.ai.ai_router import get_ai_router


class SwaggerGenerator:
    def __init__(self):
        self.router = get_ai_router()

    def generate(self, api_data: dict) -> dict:
        endpoints = api_data.get("endpoints", [])
        base_url  = api_data.get("base_url", "https://api.example.com")
        title     = api_data.get("title", "Generated API")
        version   = api_data.get("version", "1.0.0")

        system_prompt = """
You are an expert OpenAPI 3.0 specification generator.
Given a list of API endpoints, generate a complete valid OpenAPI 3.0 JSON spec.
Infer request bodies, response schemas, and parameters from endpoint names and summaries.
Return ONLY valid JSON — no explanation, no markdown.
"""
        user_msg = f"""
Generate a complete OpenAPI 3.0 spec for this API:

Title:    {title}
Version:  {version}
Base URL: {base_url}

Endpoints:
{json.dumps([
    {
        'method':       e.get('method'),
        'path':         e.get('path'),
        'summary':      e.get('summary', ''),
        'description':  e.get('description', ''),
        'request_body': e.get('request_body', {}),
        'responses':    e.get('responses', {}),
        'parameters':   e.get('parameters', [])
    }
    for e in endpoints
], indent=2)}
"""
        result = self.router.chat_json(system_prompt, user_msg)

        try:
            spec = json.loads(result)
            return spec
        except Exception:
            return self._fallback_spec(title, version, base_url, endpoints)

    def save(self, spec: dict, output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        return output_path

    def generate_fastapi_code(self, spec: dict) -> str:
        title   = spec.get("info", {}).get("title", "Generated API")
        version = spec.get("info", {}).get("version", "1.0.0")
        paths   = spec.get("paths", {})

        routes = []
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() not in ["GET","POST","PUT","PATCH","DELETE"]:
                    continue
                func_name = path.replace("/", "_").replace("{", "").replace("}", "").strip("_")
                func_name = f"{method.lower()}_{func_name}" if func_name else f"{method.lower()}_root"
                summary   = details.get("summary", "")
                routes.append(f"""
@app.{method.lower()}("{path}", summary="{summary}")
async def {func_name}():
    # TODO: implement
    return {{"message": "ok"}}
""")

        code = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{title}",
    version="{version}",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

{"".join(routes)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        return code

    def _fallback_spec(self, title, version, base_url, endpoints) -> dict:
        paths = {}
        for e in endpoints:
            path   = e.get("path", "/")
            method = e.get("method", "GET").lower()
            if path not in paths:
                paths[path] = {}
            paths[path][method] = {
                "summary":   e.get("summary", ""),
                "responses": {"200": {"description": "Success"}}
            }

        return {
            "openapi": "3.0.0",
            "info": {
                "title":   title,
                "version": version
            },
            "servers": [{"url": base_url}],
            "paths":   paths
        }
