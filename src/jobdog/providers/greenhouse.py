from urllib.parse import urlparse, urlunparse
from jobdog.models.job_listing import JobListing
from jobdog.providers.base import BaseParser
from jobdog.providers.utils import register_parser
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.logger import debug, error, info, warn


@register_parser("greenhouse.io")
class GreenhouseParser(BaseParser):
    def sanitize_url(self, url: str) -> str:
        debug(f"Sanitizing Greenhouse job URL: {url}")
        parsed_url = urlparse(url)

        try:
            # Cant strip subdomain, so much be either 'boards' or 'job-boards'
            subdomain = parsed_url.netloc.split(".")[0]
            if subdomain not in ["boards", "job-boards"]:
                raise JobDogSanitizeUrlError(
                    f"Invalid Greenhouse job URL: {url}. Subdomain must be 'boards' or 'job-boards'."
                )

            path_parts = parsed_url.path.strip("/").split("/")
            if len(path_parts) < 3 or path_parts[-2] != "jobs":
                raise JobDogSanitizeUrlError(
                    f"Invalid Greenhouse job URL format: {url}"
                )

            company_name = path_parts[0]
            job_id = path_parts[-1]

            new_path = f"/{company_name}/jobs/{job_id}"
            new_parsed = parsed_url._replace(path=new_path, query="", fragment="")
            sanitized_url = urlunparse(new_parsed)

            info(f"Sanitized Greenhouse job URL: {sanitized_url}")
            return sanitized_url
        except Exception as e:
            error(f"Error sanitizing Greenhouse job URL: {url}. Error: {str(e)}")
            raise JobDogSanitizeUrlError(
                f"Error sanitizing Greenhouse job URL: {url}. Error: {str(e)}"
            )

    def parse_html(self, html: str) -> JobListing:
        pass
