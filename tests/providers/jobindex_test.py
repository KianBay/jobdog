import pytest
from jobdog.exceptions import JobDogSanitizeUrlError
from jobdog.logger import logger
from jobdog.models.job_listing import JobListing
from jobdog.jobdog import JobDog
from jobdog.providers.jobindex import JobIndexParser
from jobdog.http_client import sync_http_client
from tests.conftest import cassette_id_func

JOBINDEX_SHORT_URLS = {
    "novo_nordisk": "https://www.jobindex.dk/jobannonce/r12800344",
    "arla": "https://www.jobindex.dk/jobannonce/h1509671",
}

JOBINDEX_URL_TEST_CASES = [
    (
        "https://www.jobindex.dk/jobannonce/r12800344/pilot-scientist-for-purification",
        "https://www.jobindex.dk/jobannonce/r12800344",
    ),
    (
        "https://www.jobindex.dk/jobannonce/h1509671/international-export-manager-distributor-sales-copenhagen",
        "https://www.jobindex.dk/jobannonce/h1509671",
    ),
]


JOBINDEX_PARSE_TEST_CASES = [
    (
        JOBINDEX_SHORT_URLS["novo_nordisk"],
        {
            "job_title": "Pilot Scientist for Purification",
            "company_name": "Novo Nordisk A/S",
            "job_description": "As Pilot Scientist you are responsible for driving production campaigns in the facility. That includes planning, dimensioning",
            "location": "2880 Bagsværd",
            "job_posting_date": "2024-10-18",
        },
    ),
    (
        JOBINDEX_SHORT_URLS["arla"],
        {
            "job_title": "International Export Manager, Distributor Sales - Copenhagen",
            "company_name": "Arla Foods",
            "job_description": "As the new International Export Manager, your main role will be to ensure exceptional sales performance and build branded positions in your market cluster.",
            "location": "Copenhagen",
        },
    ),
]


@pytest.mark.parametrize("url, expected_url", JOBINDEX_URL_TEST_CASES)
def test_jobindex_sanitize_url_success(url: str, expected_url: str):
    parser = JobIndexParser()
    assert parser.sanitize_url(url) == expected_url


@pytest.mark.parametrize(
    "invalid_url",
    [
        "https://www.example.com/not-jobindex",
        "https://www.jobindex.dk/vis-job/r12800344",
        "https://www.jobindex.dk/jobannonce/invalid-job-id",
    ],
)
def test_jobindex_sanitize_url_error(invalid_url: str):
    parser = JobIndexParser()
    with pytest.raises(JobDogSanitizeUrlError):
        parser.sanitize_url(invalid_url)


@pytest.mark.parametrize(
    "url, expected_data", JOBINDEX_PARSE_TEST_CASES, ids=cassette_id_func
)
@pytest.mark.vcr()
def test_jobindex_parse_html(url, expected_data):
    parser = JobIndexParser()
    resp = sync_http_client.get(url)

    logger.info(f"Response code: {resp.status_code}")
    logger.info(f"Response text length: {len(resp.text)}")

    job_listing = parser.parse_html(resp.text)
    logger.info(f"Job listing: {job_listing}")
    assert isinstance(job_listing, JobListing)
    assert job_listing.job_title == expected_data["job_title"]
    assert job_listing.company_name == expected_data["company_name"]
    assert expected_data["job_description"] in job_listing.job_description
