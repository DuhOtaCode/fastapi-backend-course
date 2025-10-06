from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import requests


class BaseHTTPClient(ABC):
    def __init__(self) -> None:
        self.session = requests.Session()
        self.base_url, self.headers, self.timeout = self.build_base()

    @abstractmethod
    def build_base(self) -> Tuple[str, Dict[str, str], int]:
        pass

    def parse_response(self, resp: requests.Response) -> Any:
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text

    def _join(self, path: str) -> str:
        if not path:
            return self.base_url
        if self.base_url.endswith("/") and path.startswith("/"):
            return self.base_url[:-1] + path
        if not self.base_url.endswith("/") and not path.startswith("/"):
            return self.base_url + "/" + path
        return self.base_url + path

    def request(self, method: str, path: str = "", **kwargs) -> Any:
        kwargs.setdefault("headers", self.headers)
        kwargs.setdefault("timeout", self.timeout)
        resp = self.session.request(method, self._join(path), **kwargs)
        return self.parse_response(resp)


    def get(self, path: str = "", **kw) -> Any:   return self.request("GET", path, **kw)
    def post(self, path: str = "", **kw) -> Any:  return self.request("POST", path, **kw)
    def put(self, path: str = "", **kw) -> Any:   return self.request("PUT", path, **kw)
    def patch(self, path: str = "", **kw) -> Any: return self.request("PATCH", path, **kw)
