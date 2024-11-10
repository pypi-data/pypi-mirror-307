__all__ = [
    "fetch"
    "get_user_agent"
]

import http.client
import random
from typing import Dict, Any
import json

def get_user_agent() -> str:
    return random.choice(
        fetch(host="jnrbsn.github.io",
              path="/user-agents/user-agents.json")
    )

def fetch(host: None | str, 
          path: None | str,
          method: str = "GET",
          headers: Dict[str, str] = {},
          params: Dict[str, str] = {},
          spoof: bool = False,
          raw: bool = False) -> Any:
    
    if spoof:
        headers["User-Agent"] = get_user_agent()
        
    if params:
        path += "?" + "&".join(f"{key}={value}" for key, value in params.items()).replace(" ", "%20")
    
    conn = http.client.HTTPSConnection(host)
    conn.request(method.upper(), path, headers=headers)
    response = conn.getresponse()

    if raw:
        return response
    if response.status == 200:
        return json.loads(response.read().decode('utf-8'))
    
    raise ValueError(f"Error {response.status}: {response.reason}")