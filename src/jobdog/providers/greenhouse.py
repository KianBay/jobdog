from html import unescape
import json
import re
from typing import Optional

from selectolax.parser import HTMLParser
from urllib.parse import urlparse, urlunparse
from jobdog.models.job_listing import JobListing
from jobdog.providers.base import BaseParser
from jobdog.providers.utils import register_parser
from jobdog.exceptions import JobDogSanitizeUrlError, ParserError
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
        tree = HTMLParser(html)
        json_ld = self._extract_json_ld(tree)

        job_data = {
            "job_title": self._extract_job_title(json_ld, tree),
            "company_name": self._extract_company_name(json_ld, tree),
            "job_description": self._extract_job_description(json_ld, tree),
            "location": self._extract_location(json_ld, tree),
            "job_posting_date": self._extract_job_posting_date(json_ld),
        }

        return JobListing(**job_data)

    def _extract_json_ld(self, tree: HTMLParser) -> Optional[dict]:
        script_tag = tree.css_first('script[type="application/ld+json"]')
        if script_tag:
            return json.loads(script_tag.text())
        return None

    def _extract_job_title(self, json_ld: Optional[dict], tree: HTMLParser) -> str:
        if json_ld:
            job_title = json_ld.get("title")
            if job_title:
                return job_title

        title_elem = tree.css_first("div.job__title h1")
        if not title_elem:
            raise ParserError("Failed to find title element")
        job_title = title_elem.text().strip()
        if job_title:
            return job_title
        raise ParserError("Failed to extract job title")

    def _extract_company_name(self, json_ld: Optional[dict], tree: HTMLParser) -> str:
        if json_ld:
            company_name = json_ld.get("hiringOrganization", {}).get("name")
            if company_name:
                return company_name

        title_elem = tree.css_first("title")
        if not title_elem:
            raise ParserError("Failed to find title element")
        # elem is "Job Application for <job title> at <company name>"
        full_title = title_elem.text().strip()
        if not full_title.startswith("Job Application for "):
            raise ParserError(f"Unexpected title format: {full_title}")
        full_title = full_title[len("Job Application for ") :]

        parts = full_title.split(" at ")
        if len(parts) < 2:
            raise ParserError(f"Unexpected title format: {full_title}")

        company_name = parts[-1].strip()
        if company_name:
            return company_name
        raise ParserError("Failed to extract company name")

    def _extract_job_description(
        self, json_ld: Optional[dict], tree: HTMLParser
    ) -> str:
        if json_ld:
            job_description = json_ld.get("description")
            if job_description:
                unescaped = unescape(job_description)
                # we might need to use a better method than regex'ing out html shit
                return re.sub(r"<[^>]+>", "", unescaped)

        description_div = tree.css_first("div.job__description.body")
        if not description_div:
            raise ParserError("Failed to find job description div")

        content = []
        for elem in description_div.css("p, ul, ol"):
            if elem.tag == "p":
                content.append(elem.text(strip=True))
            elif elem.tag in ("ul", "ol"):
                list_items = [
                    li.text(strip=True) for li in elem.css("li") if li.text(strip=True)
                ]
                content.append("\n".join(f"• {item}" for item in list_items))

        description = "\n\n".join(item for item in content if item)

        return description

    def _extract_location(self, json_ld: Optional[dict], tree: HTMLParser) -> list[str]:
        location_elems = tree.css("div.location")
        if location_elems:
            location_text = location_elems[0].text().strip()
            return self._parse_location_text(location_text)

        # seems to be in .body--metadata for 'job-boards' subdomain
        metadata_elem = tree.css_first(".body--metadata")
        if metadata_elem:
            location_text = metadata_elem.text().strip()
            return self._parse_location_text(location_text)

        raise ParserError("No location elements found")

    def _parse_location_text(self, location_text: str) -> list[str]:
        if "|" in location_text:
            return [loc.strip() for loc in location_text.split("|") if loc.strip()]
        elif ";" in location_text:
            return [loc.strip() for loc in location_text.split(";") if loc.strip()]
        else:
            return [location_text]

    def _extract_job_posting_date(self, json_ld: Optional[dict]) -> Optional[str]:
        if json_ld:
            return json_ld.get("datePosted")
        return None
