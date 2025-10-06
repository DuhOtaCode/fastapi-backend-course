import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

class JsonBinStorage:
    def __init__(self):
        self.url = f"https://api.jsonbin.io/v3/b/{os.getenv('JSONBIN_ID')}"
        self.headers = {
            "X-Master-Key": os.getenv("JSONBIN_API_KEY"),
            "Content-Type": "application/json",
        }

    def load(self):
        r = requests.get(f"{self.url}/latest", headers=self.headers, timeout=10)
        r.raise_for_status()
        record = r.json().get("record", [])
        if isinstance(record, str):
            try:
                record = json.loads(record)
            except json.JSONDecodeError:
                record = []
        if isinstance(record, dict) and "record" in record:
            record = record["record"]
        return [t for t in record if isinstance(t, dict)]

    def save(self, data):
        if not isinstance(data, list):
            raise TypeError("save() принимает только список задач")
        payload = {"record": data}
        r = requests.put(self.url, json=payload, headers=self.headers, timeout=10)
        r.raise_for_status()
        return r.json()