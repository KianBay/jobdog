from typing import Optional, Dict
from httpx import Client
from .exceptions import FetchError
from .logger import logger
from .models.job_listing import JobListing
from .providers.utils import get_parser
from .providers.base import BaseParser


class JobDog:
    def __init__(
        self,
        mounts: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> None:
        self.mounts = mounts or {}
        self.headers = headers or {}
        self.timeout = timeout
        self.http_client = self._create_http_client()

    def _create_http_client(self) -> Client:
        logger.info(
            f"Creating client: {self.mounts}, headers: {self.headers}, timeout: {self.timeout}"
        )
        return Client(
            mounts=self.mounts,
            headers=self.headers,
            timeout=self.timeout,
        )

    def fetch_details(self, url: str) -> JobListing:
        try:
            logger.info(f"Fetching details for {url}")
            parser: BaseParser = get_parser(url)
            sanitized_url = parser.sanitize_url(url)
            response = self.http_client.get(sanitized_url)
            response.raise_for_status()
            job_details: JobListing = parser.parse_html(response.text)
            job_details.job_listing_url = sanitized_url
            return job_details
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise FetchError(f"Failed to fetch URL: {url}. Error: {str(e)}")

    def set_mounts(self, mounts: Dict[str, str]) -> None:
        self.mounts = mounts
        self.http_client = self._create_http_client()

    def set_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
        self.http_client.headers.update(headers)

    def set_timeout(self, timeout: int) -> None:
        self.timeout = timeout
        self.http_client.timeout = timeout

    def close(self) -> None:
        logger.info("Attempting to close session")
        if self.http_client:
            self.http_client.close()
            logger.info("Session closed")

    def __enter__(self) -> "JobDog":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
