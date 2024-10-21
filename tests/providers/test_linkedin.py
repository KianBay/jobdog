import pytest
from jobdog.logger import logger
from jobdog.providers.linkedin import LinkedInParser
from jobdog.models.job_listing import JobListing
from jobdog.jobdog import JobDog
from tests.conftest import cassette_id_func

LINKEDIN_SHORT_URLS = {
    "openai": "https://www.linkedin.com/jobs/view/3915648739/",
    "anthropic": "https://www.linkedin.com/jobs/view/4053542511/",
}

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

LINKEDIN_PARSE_TEST_CASES = [
    (
        LINKEDIN_SHORT_URLS["openai"],
        {
            "job_title": "Machine Learning Engineer, Applied AI",
            "company_name": "OpenAI",
            "job_description": "You'll contribute to deploying state-of-the-art models in production environments, helping turn research breakthroughs into tangible solutions.",  # Add a snippet of the expected description
            "location": "San Francisco, CA",
            "employment_type": "Full-time",
            "experience_level": "Entry level",
            "apply_url": "",
            "listing_created_at": "",
            "listing_expires_at": "",
            "skills": [],
        },
    ),
    (
        LINKEDIN_SHORT_URLS["anthropic"],
        {
            "job_title": "Machine Learning Systems Engineer, RL Engineering",
            "company_name": "Anthropic",
            "job_description": "You want to build the cutting-edge systems that train AI models like Claude.",
            "job_function": "Engineering and Information Technology",
            "location": "Seattle, WA",
            "location_type": "Hybrid",
            "employment_type": "Full-time",
            "experience_level": "Entry level",
            # companyApplyUrl
            "apply_url": "https://boards.greenhouse.io/anthropic/jobs/4182383008",
            # epochAt=1729209600000
            "listing_created_at": "2024-10-18",
            # expiresAt=1737590400000
            "listing_expires_at": "2025-01-23",
            # Skills may not be visible anonymously
            # "skills": [
            #     "Algorithms",
            #     "Data Engineering",
            #     "Deep Learning",
            #     "High Performance Computing (HPC)",
            #     "Machine Learning Algorithms",
            #     "Natural Language Processing (NLP)",
            #     "Reinforcement Learning",
            #     "Reliability",
            #     "Research Skills",
            # ],
            "industry": "Research Services",
        },
    ),
]


@pytest.mark.parametrize("url, expected_url", LINKEDIN_URL_TEST_CASES)
def test_linkedin_sanitize_url(url: str, expected_url: str):
    parser = LinkedInParser()
    assert parser.sanitize_url(url) == expected_url


@pytest.mark.parametrize(
    "url, expected_data", LINKEDIN_PARSE_TEST_CASES, ids=cassette_id_func
)
@pytest.mark.vcr()
def test_linkedin_parse_html(url, expected_data):
    parser = LinkedInParser()
    dog = JobDog()

    logger.info(f"Fetching job listing from {url}")

    response = dog.http_client.get(url)

    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text length: {len(response.text)}")

    job_listing = parser.parse_html(response.text)

    assert isinstance(job_listing, JobListing)
    assert job_listing.job_title == expected_data["job_title"]
    assert job_listing.company_name == expected_data["company_name"]
    assert expected_data["job_description"] in job_listing.job_description

    logger.info(f"Parsed job listing: {job_listing}")
