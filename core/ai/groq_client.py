from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL


class GroqClient:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set in .env")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model  = GROQ_MODEL

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()

    def chat_json(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=800,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "\nRespond ONLY in valid JSON."},
                {"role": "user",   "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
