import json
import os
from core.ai.ai_router import get_ai_router


class BoilerplateGenerator:
    def __init__(self):
        self.router = get_ai_router()
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        path = os.path.join(
            os.path.dirname(__file__),
            "prompts", "boilerplate_generator.md"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def generate(self, stack: dict, requirements: dict) -> dict:
        user_msg = f"""
Generate a complete project boilerplate for this stack:

Recommended Stack:
{json.dumps(stack.get('recommended_stack', {}), indent=2)}

Project Summary: {requirements.get('summary', '')}

Core Features:
{json.dumps(requirements.get('core_features', []), indent=2)}

Suggested Endpoints:
{json.dumps(requirements.get('suggested_endpoints', [])[:5], indent=2)}
"""
        result = self.router.chat_json(self.prompt, user_msg)

        try:
            data = json.loads(result)
            if "folder_structure" not in data:
                return self._fallback(stack)
            return data
        except Exception:
            return self._fallback(stack)

    def _fallback(self, stack: dict) -> dict:
        framework = stack.get("recommended_stack", {}).get("api_framework", "FastAPI")
        return {
            "project_name": "my_api_project",
            "stack": stack.get("recommended_stack", {}),
            "folder_structure": [
                {"path": "app/",         "purpose": "Main application"},
                {"path": "app/routers/", "purpose": "API routes"},
                {"path": "app/models/",  "purpose": "Data models"},
                {"path": "app/schemas/", "purpose": "Pydantic schemas"},
                {"path": "tests/",       "purpose": "Test files"}
            ],
            "key_files": [
                {
                    "path":            "main.py",
                    "purpose":         "Entry point",
                    "content_snippet": f"from fastapi import FastAPI\napp = FastAPI()"
                }
            ],
            "dependencies": [
                {"package": "fastapi",   "version": "0.111.0", "purpose": "Web framework"},
                {"package": "uvicorn",   "version": "0.30.0",  "purpose": "ASGI server"},
                {"package": "pydantic",  "version": "2.7.0",   "purpose": "Data validation"}
            ],
            "env_variables": [
                {"key": "DATABASE_URL", "example": "postgresql://user:pass@localhost/db", "required": True},
                {"key": "SECRET_KEY",   "example": "your-secret-key",                    "required": True}
            ],
            "quick_start": [
                {"step": 1, "command": "pip install -r requirements.txt", "description": "Install dependencies"},
                {"step": 2, "command": "uvicorn main:app --reload",       "description": "Start server"}
            ]
        }
