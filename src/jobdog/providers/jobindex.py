from urllib.parse import urlparse, urlunparse
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.logger import debug, info, warn, error
from jobdog.models.job_listing import JobListing
from jobdog.providers.base import BaseParser


class JobIndexParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        debug(f"Sanitizing JobIndex job URL: {url}")
        parsed_url = urlparse(url)
        path = parsed_url.path
        try:
            path_parts = path.split("/")
            for part in path_parts:
                if (
                    part.startswith("r")
                    and part[1:].isdigit()
                    or part.startswith("h")
                    and part[1:].isdigit()
                ):
                    job_id = part
                    debug(f"Extracted job ID {job_id} from path")
                    new_path = f"/jobannonce/{job_id}"
                    new_parsed = parsed_url._replace(
                        path=new_path, query="", fragment=""
                    )
                    sanitized_url = urlunparse(new_parsed)
                    info(f"Sanitized JobIndex job URL: {sanitized_url}")
                    return sanitized_url

            warn(f"Unable to extract job ID from JobIndex URL: {url}")
            raise JobDogSanitizeUrlError(f"Invalid JobIndex job URL: {url}")
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
