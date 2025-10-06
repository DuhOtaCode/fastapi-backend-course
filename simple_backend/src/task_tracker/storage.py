import os
import json
from typing import Any, Dict, List, Tuple
from dotenv import load_dotenv
from base_http import BaseHTTPClient

load_dotenv()


class JsonBinStorage(BaseHTTPClient):
    def build_base(self) -> Tuple[str, Dict[str, str], int]:
        bin_id  = os.getenv("JSONBIN_ID")
        api_key = os.getenv("JSONBIN_API_KEY")
        if not bin_id or not api_key:
            raise ValueError("Не заданы JSONBIN_ID/JSONBIN_API_KEY")
        base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {"X-Master-Key": api_key, "Content-Type": "application/json"}
        return base_url, headers, 10

    def _normalize(self, record: Any) -> List[Dict]:
        if isinstance(record, str):
            try:
                record = json.loads(record)
            except json.JSONDecodeError:
                return []
        if isinstance(record, dict) and "record" in record:
            record = record["record"]
        if isinstance(record, list):
            return [t for t in record if isinstance(t, dict)]
        return []

    def load(self) -> List[Dict]:
        data = self.get("/latest")
        record = data.get("record", []) if isinstance(data, dict) else []
        return self._normalize(record)

    def save(self, tasks: List[Dict]) -> Dict:
        if not isinstance(tasks, list):
            raise TypeError("save() принимает только список задач")
        payload = {"record": tasks}
        return self.put(json=payload)
