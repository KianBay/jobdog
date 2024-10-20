from urllib.parse import parse_qs, urlparse, urlunparse
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.providers.base import BaseParser
from jobdog.models.job_listing import JobListing

from jobdog.logger import info


class LinkedInParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if query and "currentJobId" in query:
            job_id = query["currentJobId"][0]
        elif path.startswith("/jobs/view/"):
            job_id = path.split("/")[-1].split("-")[-1].split("?")[0]
            info(f"Extracted job ID from LinkedIn URL: {job_id}")
        else:
            raise JobDogSanitizeUrlError(f"Invalid LinkedIn job URL: {url}")

        new_path = f"/jobs/view/{job_id}/"
        new_parsed = parsed_url._replace(path=new_path, query="", fragment="")
        return urlunparse(new_parsed)

    def parse_html(self, html: str) -> JobListing:
        pass
