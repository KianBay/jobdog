import pytest
from jobdog.jobdog import JobDog
from jobdog.models.job_listing import JobListing
from jobdog.exceptions import FetchError
from unittest.mock import patch, MagicMock


def test_jobdog_initialization():
    dog = JobDog()
    assert dog.http_client is not None
    assert "python-httpx" not in dog.http_client.headers["User-Agent"]


@patch("jobdog.jobdog.get_parser")
def test_fetch_details_success(mock_get_parser):
    mock_parser = MagicMock()
    mock_parser.sanitize_url.return_value = "https://example.com/job/123"
    mock_parser.parse_html.return_value = JobListing(
        job_title="Likeable Superhero",
        company_name="NotVought",
        job_description="You will not be evil",
        job_listing_url="https://example.com/job/123",
    )
    mock_get_parser.return_value = mock_parser

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "<html>Job details</html>"
    mock_client.get.return_value = mock_response

    dog = JobDog(http_client=mock_client)
    result = dog.fetch_details("https://example.com/job/123")

    assert isinstance(result, JobListing)
    assert result.job_title == "Likeable Superhero"
    assert result.company_name == "NotVought"
    assert result.job_description == "You will not be evil"
    assert result.job_listing_url == "https://example.com/job/123"

    mock_client.get.assert_called_once_with("https://example.com/job/123")


@patch("jobdog.jobdog.get_parser")
def test_fetch_details_error(mock_get_parser):
    mock_parser = MagicMock()
    mock_parser.sanitize_url.return_value = "https://example.com/job/123"
    mock_get_parser.return_value = mock_parser

    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Connection error")

    dog = JobDog(http_client=mock_client)
    with pytest.raises(
        FetchError,
        match="Failed to fetch URL: https://example.com/job/123. Error: Connection error",
    ):
        dog.fetch_details("https://example.com/job/123")


def test_context_manager():
    mock_client = MagicMock()

    with JobDog(http_client=mock_client) as dog:
        assert dog.http_client is mock_client

    mock_client.close.assert_called_once()
