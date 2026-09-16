from core.ai.ai_router import get_ai_router
import json


class DeploymentAdvisor:
    def __init__(self):
        self.router = get_ai_router()

    def advise(self, stack: dict, requirements: dict) -> dict:
        system_prompt = """
You are a DevOps and cloud architecture expert.
Given a tech stack and project requirements, provide deployment recommendations.
Return ONLY valid JSON in this format:
{
  "recommended_platform": "AWS ECS",
  "reason": "Why this platform fits",
  "alternatives": ["Docker Compose", "GCP Cloud Run"],
  "estimated_cost": "-100/month",
  "docker_compose": "version: '3.8'\\nservices:\\n  app:\\n    build: .\\n    ports:\\n      - '8000:8000'",
  "deployment_steps": [
    {"step": 1, "action": "Build Docker image", "command": "docker build -t myapp ."},
    {"step": 2, "action": "Run container",      "command": "docker run -p 8000:8000 myapp"}
  ],
  "env_checklist": ["DATABASE_URL", "SECRET_KEY", "API_KEY"]
}
"""
        user_msg = f"""
Recommend deployment strategy for:

Stack:
{json.dumps(stack.get('recommended_stack', {}), indent=2)}

Project: {requirements.get('project_name', 'Unknown')}
Summary: {requirements.get('summary', '')}
Expected Users: {requirements.get('non_functional', {}).get('expected_users', 'unknown')}
"""
        result = self.router.chat_json(system_prompt, user_msg)

        try:
            data = json.loads(result)
            if "recommended_platform" not in data:
                return self._fallback()
            return data
        except Exception:
            return self._fallback()

    def generate_dockerfile(self, stack: dict) -> str:
        framework = stack.get("recommended_stack", {}).get("api_framework", "FastAPI")
        return f"""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _fallback(self) -> dict:
        return {
            "recommended_platform": "Docker",
            "reason":               "Universal, portable, works anywhere",
            "alternatives":         ["AWS ECS", "GCP Cloud Run"],
            "estimated_cost":       "Varies",
            "docker_compose":       "version: '3.8'\nservices:\n  app:\n    build: .\n    ports:\n      - '8000:8000'",
            "deployment_steps": [
                {"step": 1, "action": "Build image",  "command": "docker build -t myapp ."},
                {"step": 2, "action": "Run container", "command": "docker run -p 8000:8000 myapp"}
            ],
            "env_checklist": ["DATABASE_URL", "SECRET_KEY"]
        }
