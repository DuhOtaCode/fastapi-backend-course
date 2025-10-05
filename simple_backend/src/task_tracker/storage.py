import requests
import os
from dotenv import load_dotenv

load_dotenv()


class JsonBinStorage:
    def __init__(self):
        self.bin_id = os.getenv("JSONBIN_ID")
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"

        if not self.bin_id or not self.api_key:
            raise ValueError("Не заданы переменные окружения JSONBIN_ID и JSONBIN_API_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
        }

    def load(self):
        r = requests.get(f"{self.url}/latest", headers=self.headers)
        r.raise_for_status()
        return r.json()["record"]

    def save(self, data):
        r = requests.put(self.url, json=data, headers=self.headers)
        r.raise_for_status()
        return r.json()