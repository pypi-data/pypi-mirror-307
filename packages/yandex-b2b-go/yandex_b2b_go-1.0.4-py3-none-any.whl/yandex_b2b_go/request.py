from typing import Any, Dict, Optional


class Request:
    def __init__(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.method = method
        self.endpoint = endpoint
        self.params = params
        self.data = data
        self.headers: Dict[str, str] = headers or {}
