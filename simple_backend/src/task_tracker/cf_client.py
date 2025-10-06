import os
from typing import Any, Dict, Tuple
from dotenv import load_dotenv
from base_http import BaseHTTPClient

load_dotenv()


class CloudflareLLM(BaseHTTPClient):
    def build_base(self) -> Tuple[str, Dict[str, str], int]:
        account_id = os.getenv("CF_ACCOUNT_ID")
        api_token  = os.getenv("CF_API_TOKEN")
        model      = os.getenv("CF_MODEL", "@cf/meta/llama-3.1-8b-instruct")
        if not account_id or not api_token:
            raise ValueError("Нет CF_ACCOUNT_ID или CF_API_TOKEN")
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        return base_url, headers, 15

    def parse_response(self, resp) -> Any:
        data = super().parse_response(resp)
        if isinstance(data, dict):
            res = data.get("result") or {}
            text = (res.get("response") or res.get("text") or "").strip()
            return text
        return data

    def explain(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "Кратко опиши 3 шага решения пунктами."},
                {"role": "user", "content": f"Задача: {task_text}"},
            ]
        }
        return self.post(json=payload)
