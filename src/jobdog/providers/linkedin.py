from urllib.parse import parse_qs, urlparse, urlunparse
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.providers.base import BaseParser
from jobdog.models.job_listing import JobListing

from jobdog.logger import debug, error, info, warn


class LinkedInParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        debug(f"Sanitizing LinkedIn job URL: {url}")
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)
        try:
            if query and "currentJobId" in query:
                job_id = query["currentJobId"][0]
                debug(f"Extracted job ID {job_id} from query parameters")
            elif path.startswith("/jobs/view/"):
                job_id = path.split("/")[-1].split("-")[-1].split("?")[0]
                debug(f"Extracted job ID {job_id} from path")
            else:
                warn(f"Unable to extract job ID from LinkedIn URL: {url}")
                raise JobDogSanitizeUrlError(f"Invalid LinkedIn job URL: {url}")

            new_path = f"/jobs/view/{job_id}/"
            new_parsed = parsed_url._replace(path=new_path, query="", fragment="")
            sanitized_url = urlunparse(new_parsed)
            info(f"Sanitized LinkedIn job URL: {sanitized_url}")
            return sanitized_url
        except Exception as e:
            error(f"Error sanitizing LinkedIn job URL: {url}. Error: {str(e)}")
            raise JobDogSanitizeUrlError(
                f"Error sanitizing LinkedIn job URL: {url}. Error: {str(e)}"
            )

    def parse_html(self, html: str) -> JobListing:
        pass
