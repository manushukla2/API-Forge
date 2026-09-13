import requests
from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaClient:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model    = OLLAMA_MODEL
        self._check_connection()

    def _check_connection(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            r.raise_for_status()
        except Exception:
            raise ConnectionError(f"Ollama not running at {self.base_url}. Start with: ollama serve")

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "options": {"temperature": temperature},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ]
        }
        r = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()

    def chat_json(self, system_prompt: str, user_message: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.1},
            "messages": [
                {"role": "system", "content": system_prompt + "\nRespond ONLY in valid JSON."},
                {"role": "user",   "content": user_message}
            ]
        }
        r = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
