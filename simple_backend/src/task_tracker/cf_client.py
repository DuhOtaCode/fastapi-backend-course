import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CloudflareLLM:
    def __init__(self):
        self.url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{os.getenv('CF_ACCOUNT_ID')}/ai/run/{os.getenv('CF_MODEL', '@cf/meta/llama-3.1-8b-instruct')}"
        )
        self.headers = {
            "Authorization": f"Bearer {os.getenv('CF_API_TOKEN')}",
            "Content-Type": "application/json",
        }

    def explain(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "Кратко опиши 3 шага решения пунктами."},
                {"role": "user", "content": f"Задача: {task_text}"},
            ]
        }
        try:
            r = requests.post(self.url, json=payload, headers=self.headers, timeout=15)
            res = r.json().get("result", {})
            return (res.get("response") or res.get("text") or "").strip()
        except Exception:
            return ""