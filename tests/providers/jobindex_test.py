import pytest
from jobdog.logger import logger
from jobdog.models.job_listing import JobListing
from jobdog.jobdog import JobDog
from jobdog.providers.jobindex import JobIndexParser
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
    )
]


@pytest.mark.parametrize("url, expected_url", JOBINDEX_URL_TEST_CASES)
def test_jobindex_sanitize_url(url: str, expected_url: str):
    parser = JobIndexParser()
    assert parser.sanitize_url(url) == expected_url


@pytest.mark.parametrize(
    "url, expected_data", JOBINDEX_PARSE_TEST_CASES, ids=cassette_id_func
)
@pytest.mark.vcr()
def test_linkedin_parse_html(url, expected_data):
    parser = JobIndexParser()
    dog = JobDog()
