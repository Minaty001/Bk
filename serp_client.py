import requests
import json


class SerpClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = "https://serpapi.com/search.json"

    def search(self, query: str, engine: str = "google"):
        params = {
            "engine": engine,
            "q": query,
            "api_key": self.api_key,
        }
        resp = requests.get(self.base, params=params, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"SerpAPI error: {resp.status_code} {resp.text}")
        try:
            return resp.json()
        except json.JSONDecodeError:
            return {"error": "invalid json"}
