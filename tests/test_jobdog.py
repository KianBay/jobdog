import pytest
from jobdog.jobdog import JobDog
from jobdog.models.job_listing import JobListing
from jobdog.exceptions import FetchError
from unittest.mock import patch, MagicMock

def test_jobdog_initialization():
    dog = JobDog()
    assert dog.impersonate == "chrome124"
    assert dog.proxies == {}
    assert dog.headers == {}
    assert dog.timeout == 30

def test_jobdog_custom_initialization():
    dog = JobDog(impersonate="firefox110", proxies={"http": "http://myproxy:8080", "https": "http://myproxy:8080"}, headers={"User-Agent": "MyBot"}, timeout=60)
    assert dog.impersonate == "firefox110"
    assert dog.proxies == {"http": "http://myproxy:8080", "https": "http://myproxy:8080"}
    assert dog.headers == {"User-Agent": "MyBot"}
    assert dog.timeout == 60

@patch('jobdog.jobdog.get_parser')
@patch('jobdog.jobdog.requests.Session')
def test_fetch_details_success(mock_session, mock_get_parser):
    mock_response = MagicMock()
    mock_response.text = "<html>Job details</html>"
    mock_session.return_value.get.return_value = mock_response

    mock_parser = MagicMock()
    mock_parser.sanitize_url.return_value = "https://example.com/job/123"
    mock_parser.parse_html.return_value = JobListing(job_title="Likeable Superhero", company_name="NotVought", job_description="You will not be evil", job_listing_url="https://example.com/job/123")
    mock_get_parser.return_value = mock_parser
    dog = JobDog()
    result = dog.fetch_details("https://example.com/job/123")
    
    assert result.job_title == "Likeable Superhero"
    assert result.company_name == "NotVought"
    assert result.job_description == "You will not be evil"
    assert result.job_listing_url == "https://example.com/job/123"
    mock_session.return_value.get.assert_called_once_with("https://example.com/job/123")

@patch('jobdog.jobdog.requests.Session')
def test_fetch_details_error(mock_session):
    mock_session.return_value.get.side_effect = Exception("Connection error")

    dog = JobDog()
    with pytest.raises(FetchError, match="Failed to fetch URL: https://example.com/job/123. Error: Connection error"):
        dog.fetch_details("https://example.com/job/123")

def test_set_impersonate():
    dog = JobDog()
    dog.set_impersonate("firefox110")
    assert dog.impersonate == "firefox110"

def test_set_proxy():
    dog = JobDog()
    dog.set_proxies({"http": "http://newproxy:8080", "https": "http://newproxy:8080"})
    assert dog.proxies == {"http": "http://newproxy:8080", "https": "http://newproxy:8080"}

def test_set_headers():
    dog = JobDog()
    dog.set_headers({"X-Custom-Header": "Value"})
    assert "X-Custom-Header" in dog.headers
    assert dog.headers["X-Custom-Header"] == "Value"

def test_set_timeout():
    dog = JobDog()
    dog.set_timeout(45)
    assert dog.timeout == 45

@patch('jobdog.jobdog.requests.Session')
def test_context_manager(mock_session):
    mock_close = MagicMock()
    mock_session.return_value.close = mock_close

    with JobDog() as dog:
        pass

    mock_close.assert_called_once()


def test_integration_fetch_details():
    dog = JobDog()
    result = dog.fetch_details("https://httpbin.org/get")

    assert result["url"] == "https://httpbin.org/get"
    assert "headers" in result["content"] 