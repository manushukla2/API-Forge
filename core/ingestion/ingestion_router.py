import os
from config.constants import InputType


def detect_input_type(source: str) -> InputType:
    """
    Source kya hai — automatically detect karo
    source = file path | URL | raw text | curl command
    """
    source = source.strip()

    # cURL command
    if source.lower().startswith("curl "):
        return InputType.CURL

    # URL
    if source.startswith("http://") or source.startswith("https://"):
        return InputType.URL

    # File path
    if os.path.isfile(source):
        ext = os.path.splitext(source)[1].lower()
        if ext in [".json"]:
            # Postman ya Swagger JSON ho sakta hai
            return _detect_json_file(source)
        elif ext in [".yaml", ".yml"]:
            return InputType.SWAGGER
        elif ext in [".pdf"]:
            return InputType.PDF

    # Plain text
    return InputType.TEXT


def _detect_json_file(filepath: str) -> InputType:
    """JSON file ke andar dekho — Postman hai ya Swagger"""
    try:
        import json
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Postman collection signature
        if "info" in data and "schema" in data.get("info", {}):
            return InputType.POSTMAN

        # Swagger/OpenAPI signature
        if "openapi" in data or "swagger" in data:
            return InputType.SWAGGER

    except Exception:
        pass

    return InputType.TEXT


def route_input(source: str) -> dict:
    """
    Input detect karo aur sahi parser se parse karo
    Returns: { "type": InputType, "data": parsed_data }
    """
    input_type = detect_input_type(source)

    if input_type == InputType.SWAGGER:
        from core.ingestion.swagger_parser import SwaggerParser
        data = SwaggerParser().parse(source)

    elif input_type == InputType.POSTMAN:
        from core.ingestion.postman_parser import PostmanParser
        data = PostmanParser().parse(source)

    elif input_type == InputType.PDF:
        from core.ingestion.pdf_parser import PDFParser
        data = PDFParser().parse(source)

    elif input_type == InputType.CURL:
        from core.ingestion.curl_parser import CurlParser
        data = CurlParser().parse(source)

    elif input_type == InputType.URL:
        from core.ingestion.url_crawler import URLCrawler
        data = URLCrawler().crawl(source)

    elif input_type == InputType.TEXT:
        from core.ingestion.text_parser import TextParser
        data = TextParser().parse(source)

    else:
        raise ValueError(f"Unsupported input type: {input_type}")

    return {
        "type":  input_type,
        "data":  data
    }
