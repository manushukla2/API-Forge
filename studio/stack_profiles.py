STACK_PROFILES = {
    "fastapi_postgres": {
        "name":        "FastAPI + PostgreSQL",
        "description": "Python REST API with relational database",
        "use_case":    "CRUD APIs, BFSI, enterprise backends",
        "components":  ["fastapi", "postgresql", "redis", "jwt_auth", "docker"],
        "stack": {
            "language":      "Python",
            "framework":     "FastAPI",
            "database":      "PostgreSQL",
            "cache":         "Redis",
            "auth":          "JWT",
            "deployment":    "Docker"
        }
    },
    "fastapi_mongo": {
        "name":        "FastAPI + MongoDB",
        "description": "Python REST API with document database",
        "use_case":    "Flexible schema, content APIs, rapid development",
        "components":  ["fastapi", "mongodb", "redis", "jwt_auth", "docker"],
        "stack": {
            "language":      "Python",
            "framework":     "FastAPI",
            "database":      "MongoDB",
            "cache":         "Redis",
            "auth":          "JWT",
            "deployment":    "Docker"
        }
    },
    "langchain_rag": {
        "name":        "LangChain RAG Pipeline",
        "description": "AI-powered retrieval augmented generation API",
        "use_case":    "Chatbots, document QA, knowledge bases",
        "components":  ["fastapi", "langchain", "vector_db", "postgresql", "jwt_auth", "docker"],
        "stack": {
            "language":      "Python",
            "framework":     "FastAPI",
            "database":      "PostgreSQL",
            "ai_layer":      "LangChain",
            "vector_store":  "Pinecone",
            "auth":          "JWT",
            "deployment":    "Docker"
        }
    },
    "langgraph_agent": {
        "name":        "LangGraph Multi-Agent",
        "description": "Stateful multi-agent AI system",
        "use_case":    "Complex AI workflows, autonomous agents",
        "components":  ["fastapi", "langgraph", "vector_db", "redis", "postgresql", "docker"],
        "stack": {
            "language":      "Python",
            "framework":     "FastAPI",
            "database":      "PostgreSQL",
            "ai_layer":      "LangGraph",
            "cache":         "Redis",
            "deployment":    "Docker"
        }
    },
    "graphql_postgres": {
        "name":        "GraphQL + PostgreSQL",
        "description": "GraphQL API with relational database",
        "use_case":    "Complex nested data, multiple frontend clients",
        "components":  ["graphql_api", "postgresql", "redis", "jwt_auth", "docker"],
        "stack": {
            "language":      "Python",
            "framework":     "Strawberry GraphQL",
            "database":      "PostgreSQL",
            "cache":         "Redis",
            "auth":          "JWT",
            "deployment":    "Docker"
        }
    },
    "serverless_aws": {
        "name":        "Serverless AWS Lambda",
        "description": "Event-driven serverless API on AWS",
        "use_case":    "Low traffic, event-driven, cost-optimized",
        "components":  ["api_gateway", "aws_lambda", "postgresql", "jwt_auth"],
        "stack": {
            "language":      "Python",
            "framework":     "AWS Lambda",
            "database":      "PostgreSQL (RDS)",
            "auth":          "JWT",
            "deployment":    "AWS SAM"
        }
    }
}


class StackProfiles:
    def get_all(self) -> dict:
        return STACK_PROFILES

    def get(self, key: str) -> dict:
        return STACK_PROFILES.get(key, {})

    def list_names(self) -> list:
        return [(k, v["name"]) for k, v in STACK_PROFILES.items()]

    def get_by_use_case(self, keyword: str) -> dict:
        keyword = keyword.lower()
        return {
            k: v for k, v in STACK_PROFILES.items()
            if keyword in v.get("use_case", "").lower()
        }
