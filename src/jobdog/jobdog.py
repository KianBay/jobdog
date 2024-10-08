from typing import Optional, Dict
from curl_cffi import requests
from .exceptions import FetchError
from .logger import logger

class JobDog:
    def __init__(self, impersonate: str = "chrome110", proxy: Optional[str] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> None:
        self.impersonate = impersonate
        self.proxy = proxy
        self.headers = headers or {}
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        return requests.Session(
            impersonate=self.impersonate,
            proxies={'http': self.proxy, 'https': self.proxy} if self.proxy else None,
            headers=self.headers,
            timeout=self.timeout
        )

    def fetch_details(self, url: str) -> Dict:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return {"url": url, "content": response.text}
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise FetchError(f"Failed to fetch URL: {url}. Error: {str(e)}")