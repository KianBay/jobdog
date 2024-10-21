from selectolax.parser import HTMLParser
from urllib.parse import urlparse, urlunparse
from jobdog.exceptions import JobDogSanitizeUrlError, ParserError
from jobdog.logger import debug, info, warn, error
from jobdog.models.job_listing import JobListing
from jobdog.providers.base import BaseParser
from jobdog.providers.utils import register_parser


@register_parser("jobindex.dk")
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
        tree = HTMLParser(html)

        job_title = self._extract_job_title(tree)
        company_name = self._extract_company_name(tree)
        job_description = self._extract_job_description(tree)

        if not all([job_title, company_name, job_description]):
            raise ParserError("Failed to extract required fields from HTML")

        return JobListing(
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
        )

    def _extract_job_title(self, tree: HTMLParser) -> str:
        title_elem = tree.css_first("h1")
        if title_elem:
            return title_elem.text().strip()
        raise ParserError("Failed to extract job title")

    def _extract_company_name(self, tree: HTMLParser) -> str:
        # h-prefixed listings
        footer_company_elem = tree.css_first(
            "div.col-xl-4:nth-child(1) > p:nth-child(1) > b:nth-child(1)"
        )
        if footer_company_elem:
            return footer_company_elem.text().strip()
        # r-prefixed listings
        company_elem = tree.css_first(
            ".jobtext-jobad__company, span.jobtext-jobad__company"
        )
        if company_elem:
            return company_elem.text().strip()

        raise ParserError("Failed to extract company name")

    def _extract_job_description(self, tree: HTMLParser) -> str:
        # r-prefixed listings
        description_elem = tree.css_first(".jobtext-jobad__body")

        # h-prefixed listings
        if not description_elem:
            description_elem = tree.css_first(
                ".col-md-10.offset-md-1.col-xl-7.offset-xl-0.pt-0.pt-md-5.mt-5.px-3.px-xxl-0"
            )

        if description_elem:
            description = ""
            for child in description_elem.iter():
                if child.tag in ["p", "ul", "ol", "h2", "h3", "h4"]:
                    description += child.text().strip() + "\n\n"
            return description.strip()

        raise ParserError("Failed to extract job description")
