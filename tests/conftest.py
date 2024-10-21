import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "record_mode": "once",
        "ignore_localhost": True,
        "allow_playback_repeats": True,
    }


def cassette_id_func(fixture_value):
    if isinstance(fixture_value, str) and "/" in fixture_value:
        return f"job_{fixture_value.split('/')[-1].split('?')[0]}"
    return fixture_value
