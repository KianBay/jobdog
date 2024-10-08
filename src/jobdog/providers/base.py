from abc import ABC, abstractmethod
from typing import Dict, Any
from jobdog.models.job_listing import JobListing
class BaseParser(ABC):
    @abstractmethod
    def sanitize_url(self, url: str) -> str:
        pass

    @abstractmethod
    def parse_html(self, html: str) -> JobListing:
        pass