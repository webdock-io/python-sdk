from __future__ import annotations
from typing import Any, Dict, Iterable,  Optional,   Type,    TypeVar
import requests
 
class RequestOptions:
    def __init__(
        self,
        *,
        token: Optional[str],
        endpoint: str,
        method: str,
        body: Optional[Any] = None,
        headers: Optional[Iterable[str]] = None,
     ) -> None:
        self.token = token
        self.endpoint = endpoint
        self.method = method
        self.body = body
        self.headers = list(headers) if headers is not None else []
 
def _format_endpoint(endpoint: str) -> str:
    if not endpoint.startswith("/"):
        return "/" + endpoint
    return endpoint

T = TypeVar("T")

def req(opts: RequestOptions, return_type: Type[T] = None) -> T:
        formatted_endpoint = _format_endpoint(opts.endpoint)
        url = f"https://api.webdock.io/v1{formatted_endpoint}"
        
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {opts.token}",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache, no-store, must-revalidate",
        }

        response = requests.request(
            opts.method,
            url,
            headers=headers,
            json=opts.body,
        )

        response.raise_for_status()
        return_headers: Dict[str, str] = {}
        for h in opts.headers:
            if h:
                return_headers[str(h).lower().replace("-", "_")] = response.headers.get(h, "")

        response_data = {
            "body": response.json() if response.content else None,
            "headers": return_headers,
        }
        
        
        return response_data

