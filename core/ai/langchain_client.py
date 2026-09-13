from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from config.settings import (
    AI_LLM,
    GROQ_API_KEY, GROQ_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    OLLAMA_BASE_URL, OLLAMA_MODEL
)


class LangChainClient:
    def __init__(self):
        self.llm = self._load_llm()

    def _load_llm(self):
        if AI_LLM == "groq":
            return ChatGroq(
                api_key=GROQ_API_KEY,
                model=GROQ_MODEL,
                temperature=0.3
            )
        elif AI_LLM == "openai":
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=OPENAI_MODEL,
                temperature=0.3
            )
        elif AI_LLM == "ollama":
            return Ollama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL
            )
        else:
            raise ValueError(f"Unsupported AI_LLM: {AI_LLM}")

    def chat(self, system_prompt: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()

    def chat_json(self, system_prompt: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_prompt + "\nRespond ONLY in valid JSON."),
            HumanMessage(content=user_message)
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()
