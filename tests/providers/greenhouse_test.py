import pytest
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.logger import logger
from jobdog.models.job_listing import JobListing
from jobdog.jobdog import JobDog
from jobdog.providers.greenhouse import GreenhouseParser
from jobdog.http_client import sync_http_client
from tests.conftest import cassette_id_func


GREENHOUSE_SHORT_URLS = {
    "anthropic": "https://boards.greenhouse.io/anthropic/jobs/4182383008",
    "scaleai": "https://job-boards.greenhouse.io/scaleai/jobs/4315289005?source=remoteai.ioutm_source=remoteai.io",
}

GREENHOUSE_URL_TEST_CASES = [
    (
        "https://boards.greenhouse.io/anthropic/jobs/4182383008",
        "https://boards.greenhouse.io/anthropic/jobs/4182383008",
    ),
    (
        "https://job-boards.greenhouse.io/scaleai/jobs/4315289005?source=remoteai.ioutm_source=remoteai.io",
        "https://job-boards.greenhouse.io/scaleai/jobs/4315289005",
    ),
]
GREENHOUSE_PARSE_TEST_CASES = [
    (
        GREENHOUSE_SHORT_URLS["anthropic"],
        {
            "job_title": "Machine Learning Systems Engineer, RL Engineering",
            "company_name": "Anthropic",
            "job_description": "Our finetuning researchers train our production Claude models, and internal research models, using RLHF and other related methods. Your job will be to build, maintain, and improve the algorithms and systems that these researchers use to train models.",
            "location": ["San Francisco, CA", "New York City, NY", "Seattle, WA"],
        },
    ),
    (
        GREENHOUSE_SHORT_URLS["scaleai"],
        {
            "job_title": "Senior/Staff Machine Learning Research Scientist Generative AI",
            "company_name": "Scale AI",
            "job_description": "You will be involved end-to-end from the inception and planning of new research agendas. You'll be creating high quality datasets, implementing models and associated training and evaluation stacks, producing high caliber publications in the form of peer-reviewed journal articles, blogs, white papers, and internal presentations & documentation.",
            "location": ["San Francisco, CA", "Seattle, WA", "New York, NY"],
        },
    ),
]


@pytest.mark.parametrize("url, expected_url", GREENHOUSE_URL_TEST_CASES)
def test_greenhouse_sanitize_url_success(url: str, expected_url: str):
    parser = GreenhouseParser()
    assert parser.sanitize_url(url) == expected_url


@pytest.mark.parametrize(
    "invalid_url",
    [
        "https://greenhouse.io/anthropic/jobs/4182383008/",
        "https://www.example.com/not-greenhouse",
    ],
)
def test_greenhouse_sanitize_url_error(invalid_url: str):
    parser = GreenhouseParser()
    with pytest.raises(JobDogSanitizeUrlError):
        parser.sanitize_url(invalid_url)


@pytest.mark.parametrize(
    "url, expected_data", GREENHOUSE_PARSE_TEST_CASES, ids=cassette_id_func
)
@pytest.mark.vcr()
def test_greenhouse_parse_html(url: str, expected_data: dict):
    parser = GreenhouseParser()
    resp = sync_http_client.get(url)
    job_listing = parser.parse_html(resp.text)

    logger.info(f"Response code: {resp.status_code}")
    logger.info(f"Response text length: {len(resp.text)}")

    assert isinstance(job_listing, JobListing)
    assert job_listing.job_title == expected_data["job_title"]
    assert job_listing.company_name == expected_data["company_name"]
    assert expected_data["job_description"] in job_listing.job_description
    logger.info(
        f"Job description first 100 characters: {job_listing.job_description[:100]  }"
    )
    logger.info(
        f"Job description last 100 characters: {job_listing.job_description[-100:]  }"
    )
    for i, location in enumerate(expected_data["location"]):
        assert location == job_listing.location[i]
