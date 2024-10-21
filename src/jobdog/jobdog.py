from typing import Optional, Dict
from httpx import Client
from jobdog.exceptions import FetchError
from jobdog.logger import logger
from jobdog.models.job_listing import JobListing
from jobdog.providers.utils import get_parser
from jobdog.providers.base import BaseParser
from jobdog.http_client import sync_http_client


class JobDog:
    def __init__(
        self,
        http_client: Optional[Client] = None,
    ) -> None:
        self.http_client = http_client or sync_http_client

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
