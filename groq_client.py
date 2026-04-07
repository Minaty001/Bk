import json
import requests


class GroqClient:
    def __init__(
        self,
        api_base: str,
        chat_model: str,
        chat_api_key: str,
        coding_model: str,
        coding_api_key: str,
        compound_model: str,
        compound_api_key: str,
    ):
        self.api_base = api_base.rstrip("/")
        self.chat_model = chat_model
        self.chat_api_key = chat_api_key or ""
        self.coding_model = coding_model
        self.coding_api_key = coding_api_key or ""
        self.compound_model = compound_model
        self.compound_api_key = compound_api_key or ""

    def chat_to_actions(self, prompt: str, timeout: int = 20):
        # Call Groq's chat model to translate NL into a structured action list.
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.chat_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.chat_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if resp.status_code != 200:
            raise RuntimeError(f"Groq chat API error: {resp.status_code} - {resp.text}")
        data = resp.json()
        content = ""
        try:
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception:
            content = ""
        if not content:
            raise ValueError("Groq chat response contained no content")
        # Best-effort parse: expect a JSON array of actions.
        try:
            actions = json.loads(content)
            if isinstance(actions, list):
                return actions
        except Exception:
            pass
        # Fallback: return a single generic action describing the content for visibility.
        return [{"type": "comment", "text": content}]
