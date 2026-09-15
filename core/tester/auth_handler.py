import requests
import base64
from config.constants import AuthType


class AuthHandler:
    def __init__(self, auth_config: dict):
        """
        auth_config examples:
        {"type": "bearer", "token": "xxx"}
        {"type": "api_key", "key": "X-API-Key", "value": "xxx"}
        {"type": "basic", "username": "user", "password": "pass"}
        {"type": "oauth2", "token_url": "...", "client_id": "...", "client_secret": "..."}
        {"type": "none"}
        """
        self.auth_config = auth_config
        self.auth_type   = auth_config.get("type", "none")

    def get_headers(self) -> dict:
        if self.auth_type == AuthType.BEARER.value:
            return {"Authorization": f"Bearer {self.auth_config.get('token', '')}"}

        elif self.auth_type == AuthType.API_KEY.value:
            key   = self.auth_config.get("key", "X-API-Key")
            value = self.auth_config.get("value", "")
            return {key: value}

        elif self.auth_type == AuthType.BASIC.value:
            username = self.auth_config.get("username", "")
            password = self.auth_config.get("password", "")
            encoded  = base64.b64encode(f"{username}:{password}".encode()).decode()
            return {"Authorization": f"Basic {encoded}"}

        elif self.auth_type == AuthType.OAUTH2.value:
            token = self._fetch_oauth2_token()
            return {"Authorization": f"Bearer {token}"}

        return {}

    def _fetch_oauth2_token(self) -> str:
        token_url     = self.auth_config.get("token_url", "")
        client_id     = self.auth_config.get("client_id", "")
        client_secret = self.auth_config.get("client_secret", "")
        scope         = self.auth_config.get("scope", "")

        if not token_url:
            raise ValueError("OAuth2 token_url is required")

        payload = {
            "grant_type":    "client_credentials",
            "client_id":     client_id,
            "client_secret": client_secret,
            "scope":         scope
        }

        try:
            r = requests.post(token_url, data=payload, timeout=15)
            r.raise_for_status()
            return r.json().get("access_token", "")
        except Exception as e:
            raise ConnectionError(f"OAuth2 token fetch failed: {e}")

    def inject(self, endpoint: dict) -> dict:
        """Endpoint dict mein auth headers inject karo"""
        headers              = endpoint.get("headers", {})
        headers.update(self.get_headers())
        endpoint["headers"]  = headers
        return endpoint
