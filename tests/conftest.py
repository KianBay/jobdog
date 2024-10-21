import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "cookie"],
        "record_mode": "once",
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    return "tests/cassettes/" + request.module.__name__
