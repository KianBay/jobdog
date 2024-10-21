import datetime
from typing import Optional
from selectolax.parser import HTMLParser

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
        info(f"Parsing HTML of length {len(html)}")
        tree = HTMLParser(html)

        job_data = {
            "job_title": self._extract_job_title(tree),
            "company_name": self._extract_company_name(tree),
            "job_description": self._extract_job_description(tree),
            "job_function": self._extract_job_function(tree),
            "job_listing_url": self.url,  # Assuming self.url is set somewhere
            "location": self._extract_location(tree),
            "location_type": self._extract_location_type(tree),
            "employment_type": self._extract_employment_type(tree),
            "experience_level": self._extract_experience_level(tree),
            "apply_url": self._extract_apply_url(tree),
            "job_posting_date": self._extract_listing_created_at(tree),
            "job_expiry_date": self._extract_listing_expires_at(tree),
            "industry": self._extract_industry(tree),
        }

        return JobListing(**job_data)

    def _extract_job_title(self, tree: HTMLParser) -> str:
        title_element = tree.css_first("h1").text().strip()
        return title_element

    def _extract_company_name(self, tree: HTMLParser) -> str:
        return tree.css_first("a.sub-nav-cta__optional-url").text().strip()

    def _extract_job_description(self, tree: HTMLParser) -> str:
        description_node = tree.css_first("div.show-more-less-html__markup")
        return description_node.text(strip=True) if description_node else ""

    def _extract_job_function(self, tree: HTMLParser) -> Optional[str]:
        job_function_node = tree.css_first(
            'li.description__job-criteria-item:contains("Function")'
        )
        if job_function_node:
            return job_function_node.css_first("span").text().strip()
        return None

    def _extract_location(self, tree: HTMLParser) -> str:
        return tree.css_first("span.sub-nav-cta__meta-text").text().strip()

    def _extract_location_type(self, tree: HTMLParser) -> Optional[str]:
        location_type_node = tree.css_first(
            'li.description__job-criteria-item:contains("Location type")'
        )
        if location_type_node:
            return location_type_node.css_first("span").text().strip()
        return None

    def _extract_employment_type(self, tree: HTMLParser) -> Optional[str]:
        employment_type_node = tree.css_first(
            'li.description__job-criteria-item:contains("Employment type")'
        )
        if employment_type_node:
            return employment_type_node.css_first("span").text().strip()
        return None

    def _extract_experience_level(self, tree: HTMLParser) -> Optional[str]:
        experience_node = tree.css_first(
            'li.description__job-criteria-item:contains("Experience")'
        )
        if experience_node:
            return experience_node.css_first("span").text().strip()
        return None

    def _extract_apply_url(self, tree: HTMLParser) -> Optional[str]:
        apply_button = tree.css_first("a.sign-up-modal__company-apply-link")
        return apply_button.attributes.get("href") if apply_button else None

    def _extract_listing_created_at(self, tree: HTMLParser) -> Optional[str]:
        script_tag = tree.css_first("script#jobPostingSchema")
        if script_tag:
            import json

            data = json.loads(script_tag.text())
            date_posted = data.get("datePosted")
            if date_posted:
                return datetime.fromisoformat(date_posted).strftime("%Y-%m-%d")
        return None

    def _extract_listing_expires_at(self, tree: HTMLParser) -> Optional[str]:
        script_tag = tree.css_first("script#jobPostingSchema")
        if script_tag:
            import json

            data = json.loads(script_tag.text())
            valid_through = data.get("validThrough")
            if valid_through:
                return datetime.fromisoformat(valid_through).strftime("%Y-%m-%d")
        return None

    def _extract_industry(self, tree: HTMLParser) -> Optional[str]:
        industry_node = tree.css_first(
            'li.description__job-criteria-item:contains("Industries")'
        )
        if industry_node:
            return industry_node.css_first("span").text().strip()
        return None
