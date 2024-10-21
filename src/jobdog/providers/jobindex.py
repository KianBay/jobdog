from urllib.parse import urlparse, urlunparse
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.logger import debug, info, warn, error
from jobdog.models.job_listing import JobListing
from jobdog.providers.base import BaseParser


class JobIndexParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        debug(f"Sanitizing JobIndex job URL: {url}")
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")

        try:
            if len(path_parts) < 3 or path_parts[1] != "jobannonce":
                raise JobDogSanitizeUrlError(f"Invalid JobIndex job URL: {url}")

            job_id = path_parts[2]
            if (
                not (job_id.startswith("r") or job_id.startswith("h"))
                or not job_id[1:].isdigit()
            ):
                raise JobDogSanitizeUrlError(f"Invalid job ID in URL: {url}")

            new_path = f"/jobannonce/{job_id}"
            new_parsed = parsed_url._replace(path=new_path, query="", fragment="")
            sanitized_url = urlunparse(new_parsed)
            info(f"Sanitized JobIndex job URL: {sanitized_url}")
            return sanitized_url

        except Exception as e:
            error(f"Error sanitizing JobIndex job URL: {url}. Error: {str(e)}")
            raise JobDogSanitizeUrlError(
                f"Error sanitizing JobIndex job URL: {url}. Error: {str(e)}"
            )

    def parse_html(self, html: str) -> JobListing:
        return JobListing(
            job_title="",
            company_name="",
            job_description="",
        )
