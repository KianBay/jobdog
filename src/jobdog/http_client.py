import random
from typing import Optional
from httpx import Client

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.1",
]


def _get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def create_default_client(
    mounts: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 30,
) -> Client:
    default_headers = headers or {}
    if "User-Agent" not in default_headers:
        default_headers["User-Agent"] = _get_random_user_agent()

    return Client(
        mounts=mounts or {},
        headers=default_headers,
        timeout=timeout,
    )


sync_http_client = create_default_client()
