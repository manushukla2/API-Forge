from enum import Enum

class AIFramework(Enum):
    DIRECT     = "direct"
    LANGCHAIN  = "langchain"
    LANGGRAPH  = "langgraph"

class AIBackend(Enum):
    GROQ       = "groq"
    OPENAI     = "openai"
    OLLAMA     = "ollama"

class InputType(Enum):
    SWAGGER    = "swagger"
    PDF        = "pdf"
    POSTMAN    = "postman"
    CURL       = "curl"
    URL        = "url"
    PROXY      = "proxy"
    TEXT       = "text"

class AuthType(Enum):
    NONE       = "none"
    API_KEY    = "api_key"
    BEARER     = "bearer"
    BASIC      = "basic"
    OAUTH2     = "oauth2"

class TestStatus(Enum):
    PENDING    = "pending"
    RUNNING    = "running"
    PASSED     = "passed"
    FAILED     = "failed"
    SKIPPED    = "skipped"

class ReportFormat(Enum):
    PDF        = "pdf"
    HTML       = "html"
    JSON       = "json"

class HTTPMethod(Enum):
    GET        = "GET"
    POST       = "POST"
    PUT        = "PUT"
    PATCH      = "PATCH"
    DELETE     = "DELETE"
    OPTIONS    = "OPTIONS"
    HEAD       = "HEAD"

class AgentType(Enum):
    SCENARIO_GENERATOR   = "scenario_generator"
    FLOW_BUILDER         = "flow_builder"
    STACK_RECOMMENDER    = "stack_recommender"
    REQUIREMENT_ANALYZER = "requirement_analyzer"
    BOILERPLATE_GENERATOR = "boilerplate_generator"
