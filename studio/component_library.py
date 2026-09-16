from config.constants import HTTPMethod


COMPONENTS = {
    "api_gateway": {
        "name":        "API Gateway",
        "category":    "infrastructure",
        "description": "Entry point for all API requests",
        "icon":        "🌐",
        "config": {
            "rate_limit":   "1000/min",
            "auth":         "JWT",
            "cors":         True
        }
    },
    "rest_api": {
        "name":        "REST API",
        "category":    "api",
        "description": "RESTful API endpoint",
        "icon":        "🔌",
        "config": {
            "method":       "GET",
            "path":         "/api/v1/",
            "auth_required": True
        }
    },
    "graphql_api": {
        "name":        "GraphQL API",
        "category":    "api",
        "description": "GraphQL endpoint",
        "icon":        "◈",
        "config": {
            "endpoint":     "/graphql",
            "playground":   True
        }
    },
    "fastapi": {
        "name":        "FastAPI Service",
        "category":    "framework",
        "description": "Python FastAPI application",
        "icon":        "⚡",
        "config": {
            "host":         "0.0.0.0",
            "port":         8000,
            "reload":       True
        }
    },
    "postgresql": {
        "name":        "PostgreSQL",
        "category":    "database",
        "description": "Relational database",
        "icon":        "🐘",
        "config": {
            "host":         "localhost",
            "port":         5432,
            "pool_size":    10
        }
    },
    "mongodb": {
        "name":        "MongoDB",
        "category":    "database",
        "description": "NoSQL document database",
        "icon":        "🍃",
        "config": {
            "host":         "localhost",
            "port":         27017
        }
    },
    "redis": {
        "name":        "Redis",
        "category":    "cache",
        "description": "In-memory cache and queue",
        "icon":        "🔴",
        "config": {
            "host":         "localhost",
            "port":         6379,
            "ttl":          3600
        }
    },
    "langchain": {
        "name":        "LangChain Agent",
        "category":    "ai",
        "description": "LangChain AI orchestration",
        "icon":        "🦜",
        "config": {
            "llm":          "groq",
            "memory":       True
        }
    },
    "langgraph": {
        "name":        "LangGraph Agent",
        "category":    "ai",
        "description": "LangGraph stateful agent",
        "icon":        "🕸️",
        "config": {
            "llm":          "groq",
            "checkpointer": True
        }
    },
    "vector_db": {
        "name":        "Vector DB",
        "category":    "ai",
        "description": "Vector store for RAG",
        "icon":        "🧮",
        "config": {
            "provider":     "pinecone",
            "dimension":    1536
        }
    },
    "jwt_auth": {
        "name":        "JWT Auth",
        "category":    "auth",
        "description": "JSON Web Token authentication",
        "icon":        "🔐",
        "config": {
            "expiry":       3600,
            "algorithm":    "HS256"
        }
    },
    "docker": {
        "name":        "Docker",
        "category":    "deployment",
        "description": "Container deployment",
        "icon":        "🐳",
        "config": {
            "port":         8000,
            "replicas":     1
        }
    },
    "aws_lambda": {
        "name":        "AWS Lambda",
        "category":    "deployment",
        "description": "Serverless function deployment",
        "icon":        "λ",
        "config": {
            "runtime":      "python3.11",
            "memory":       512,
            "timeout":      30
        }
    }
}


class ComponentLibrary:
    def get_all(self) -> dict:
        return COMPONENTS

    def get_by_category(self, category: str) -> dict:
        return {k: v for k, v in COMPONENTS.items() if v["category"] == category}

    def get_categories(self) -> list:
        return sorted(list(set(v["category"] for v in COMPONENTS.values())))

    def get(self, key: str) -> dict:
        return COMPONENTS.get(key, {})
