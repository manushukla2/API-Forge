from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in .env")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model  = OPENAI_MODEL

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
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
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "\nRespond ONLY in valid JSON."},
                {"role": "user",   "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
