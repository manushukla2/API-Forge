from config.settings import AI_FRAMEWORK, AI_LLM


class AIRouter:
    def __init__(self):
        self.client = self._load_client()

    def _load_client(self):
        if AI_FRAMEWORK == "direct":
            if AI_LLM == "groq":
                from core.ai.groq_client import GroqClient
                return GroqClient()
            elif AI_LLM == "openai":
                from core.ai.openai_client import OpenAIClient
                return OpenAIClient()
            elif AI_LLM == "ollama":
                from core.ai.ollama_client import OllamaClient
                return OllamaClient()
            else:
                raise ValueError(f"Unsupported AI_LLM: {AI_LLM}")

        elif AI_FRAMEWORK == "langchain":
            from core.ai.langchain_client import LangChainClient
            return LangChainClient()

        elif AI_FRAMEWORK == "langgraph":
            from core.ai.langgraph_client import LangGraphClient
            return LangGraphClient()

        else:
            raise ValueError(f"Unsupported AI_FRAMEWORK: {AI_FRAMEWORK}")

    def chat(self, system_prompt: str, user_message: str) -> str:
        return self.client.chat(system_prompt, user_message)

    def chat_json(self, system_prompt: str, user_message: str) -> str:
        return self.client.chat_json(system_prompt, user_message)


# Singleton — poore app mein ek hi instance
_router_instance = None

def get_ai_router() -> AIRouter:
    global _router_instance
    if _router_instance is None:
        _router_instance = AIRouter()
    return _router_instance
