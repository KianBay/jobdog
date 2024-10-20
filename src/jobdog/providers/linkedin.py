from jobdog.providers.base import BaseParser
from jobdog.models.job_listing import JobListing


class LinkedInParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        return url

    def parse_html(self, html: str) -> JobListing:
        pass
