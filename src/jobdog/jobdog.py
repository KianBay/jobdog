from typing import Optional, Dict
from curl_cffi import requests
from .exceptions import FetchError
from .logger import logger
from .models.job_listing import JobListing
from .providers.utils import get_parser
from .providers.base_parser import BaseParser

class JobDog:
    def __init__(self, impersonate: str = "chrome124", proxies: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> None:
        self.impersonate = impersonate
        self.proxies = proxies or {}
        self.headers = headers or {}
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        logger.info(f"Creating session with impersonate: {self.impersonate}, proxies: {self.proxies}, headers: {self.headers}, timeout: {self.timeout}")
        return requests.Session(
            impersonate=self.impersonate,
            proxies=self.proxies,
            headers=self.headers,
            timeout=self.timeout
        )

    def fetch_details(self, url: str) -> JobListing:
        try:
            logger.info(f"Fetching details for {url}")
            parser: BaseParser = get_parser(url)
            sanitized_url = parser.sanitize_url(url)
            response = self.session.get(sanitized_url)
            response.raise_for_status()
            job_details: JobListing = parser.parse_html(response.text)
            job_details.job_listing_url = sanitized_url
            return job_details
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise FetchError(f"Failed to fetch URL: {url}. Error: {str(e)}")

    def set_impersonate(self, impersonate: str) -> None:
        self.impersonate = impersonate
        self.session = self._create_session()

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        self.proxies = proxies
        self.session = self._create_session()

    def set_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
        self.session.headers.update(headers)

    def set_timeout(self, timeout: int) -> None:
        self.timeout = timeout
        self.session.timeout = timeout


    def close(self) -> None:
        logger.info("Attempting to close session")
        if self.session:
            self.session.close()
            logger.info("Session closed")

    def __enter__(self) -> "JobDog":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()