__all__ = [
    "search",
    "HOST"
]

from .utils import fetch, get_user_agent

HOST = "api.comick.io"

def search(title, user_agent: None | str = None):
    headers = { "User-Agent": user_agent or get_user_agent()}
    return fetch(
        host=HOST,
        path="/v1.0/search",
        params={
            "q": title
        },
        headers=headers
    )
