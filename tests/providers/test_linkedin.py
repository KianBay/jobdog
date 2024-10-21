import pytest
from jobdog.logger import logger
from jobdog.providers.linkedin import LinkedInParser
from jobdog.models.job_listing import JobListing
from jobdog.jobdog import JobDog
from tests.conftest import cassette_id_func


LINKEDIN_URL_TEST_CASES = [
    (
        "https://www.linkedin.com/jobs/search?keywords=OpenAI&location=United%2BStates&geoId=103644278&f_C=11130470&currentJobId=3915648739&position=7&pageNum=0",
        "https://www.linkedin.com/jobs/view/3915648739/",
    ),
    (
        "https://www.linkedin.com/jobs/view/machine-learning-engineer-applied-ai-at-openai-3915648739?position=7&pageNum=0&refId=J2FFceTNhN%2BMfTHSqUVAKg%3D%3D&trackingId=mEtg7ZcZkfqoalfW0JeTGg%3D%3D",
        "https://www.linkedin.com/jobs/view/3915648739/",
    ),
    (
        "https://www.linkedin.com/jobs/search?keywords=Anthropic&location=United%2BStates&geoId=103644278&f_C=74126343&currentJobId=4053542511&position=18&pageNum=0",
        "https://www.linkedin.com/jobs/view/4053542511/",
    ),
    (
        "https://www.linkedin.com/jobs/view/machine-learning-systems-engineer-rl-engineering-at-anthropic-4053542511?position=18&pageNum=0&refId=WMn%2BYysXF67ZrceO8NkadQ%3D%3D&trackingId=CnKhN3A8Scx4YZqxMEaJ7g%3D%3D",
        "https://www.linkedin.com/jobs/view/4053542511/",
    ),
]


@pytest.mark.parametrize("url, expected_url", LINKEDIN_URL_TEST_CASES)
def test_linkedin_sanitize_url(url: str, expected_url: str):
    parser = LinkedInParser()
    assert parser.sanitize_url(url) == expected_url


@pytest.mark.parametrize(
    "long_url, expected_url", LINKEDIN_URL_TEST_CASES, ids=cassette_id_func
)
@pytest.mark.vcr()
def test_linkedin_parse_html(long_url, expected_url):
    parser = LinkedInParser()
    dog = JobDog()

    logger.info(f"Fetching job listing from {expected_url}")

    response = dog.http_client.get(expected_url)

    logger.info(f"Response status code: {response.status_code}")

    job_listing = parser.parse_html(response.text)

    assert isinstance(job_listing, JobListing)
    assert job_listing.job_title
    assert job_listing.company_name
    assert job_listing.job_description

    logger.info(f"Parsed job listing: {job_listing}")
