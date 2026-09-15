import json
from core.ai.ai_router import get_ai_router


class SemanticChecker:
    def __init__(self):
        self.router = get_ai_router()

    def check(self, endpoint: dict, response: dict) -> dict:
        system_prompt = """
You are a senior QA engineer specializing in AI API testing.
Analyze the API response and check for quality issues.
Return ONLY valid JSON in this exact format:
{
  "quality_score": 85,
  "issues": [],
  "hallucination_risk": "low",
  "relevance_score": 90,
  "suggestions": []
}

quality_score: 0-100
hallucination_risk: low | medium | high
relevance_score: 0-100
issues: list of strings describing problems found
suggestions: list of strings with improvement suggestions
"""
        user_msg = f"""
Analyze this API response for quality:

Endpoint:    {endpoint.get('method')} {endpoint.get('full_url', endpoint.get('path', ''))}
Summary:     {endpoint.get('summary', '')}
Status Code: {response.get('status_code')}
Latency:     {response.get('latency_ms')}ms
Response:    {json.dumps(response.get('body', {}), indent=2)[:1000]}
"""
        result = self.router.chat_json(system_prompt, user_msg)

        try:
            data = json.loads(result)
            return {
                "quality_score":      data.get("quality_score", 0),
                "hallucination_risk": data.get("hallucination_risk", "unknown"),
                "relevance_score":    data.get("relevance_score", 0),
                "issues":             data.get("issues", []),
                "suggestions":        data.get("suggestions", [])
            }
        except Exception:
            return {
                "quality_score":      0,
                "hallucination_risk": "unknown",
                "relevance_score":    0,
                "issues":             ["Could not analyze response"],
                "suggestions":        []
            }

    def check_ai_response(self, prompt: str, response_text: str) -> dict:
        system_prompt = """
You are an AI safety and quality expert.
Analyze if an AI response shows signs of hallucination or quality issues.
Return ONLY valid JSON:
{
  "hallucination_detected": false,
  "confidence": 90,
  "issues": [],
  "explanation": "Response looks accurate and relevant"
}
"""
        user_msg = f"""
Original Prompt: {prompt[:500]}

AI Response: {response_text[:1000]}
"""
        result = self.router.chat_json(system_prompt, user_msg)

        try:
            return json.loads(result)
        except Exception:
            return {
                "hallucination_detected": False,
                "confidence":             0,
                "issues":                 ["Analysis failed"],
                "explanation":            ""
            }
