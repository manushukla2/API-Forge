from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
import operator
from config.settings import (
    AI_LLM,
    GROQ_API_KEY, GROQ_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    OLLAMA_BASE_URL, OLLAMA_MODEL
)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    output:   str


class LangGraphClient:
    def __init__(self):
        self.llm   = self._load_llm()
        self.graph = self._build_graph()

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

    def _build_graph(self) -> StateGraph:
        def agent_node(state: AgentState) -> AgentState:
            response = self.llm.invoke(state["messages"])
            return {
                "messages": [response],
                "output":   response.content.strip()
            }

        graph = StateGraph(AgentState)
        graph.add_node("agent", agent_node)
        graph.set_entry_point("agent")
        graph.add_edge("agent", END)
        return graph.compile()

    def chat(self, system_prompt: str, user_message: str) -> str:
        result = self.graph.invoke({
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ],
            "output": ""
        })
        return result["output"]

    def chat_json(self, system_prompt: str, user_message: str) -> str:
        result = self.graph.invoke({
            "messages": [
                SystemMessage(content=system_prompt + "\nRespond ONLY in valid JSON."),
                HumanMessage(content=user_message)
            ],
            "output": ""
        })
        return result["output"]
