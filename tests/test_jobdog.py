import pytest
from jobdog.jobdog import JobDog

def test_jobdog_initialization():
    dog = JobDog()
    assert dog.proxy is None
    assert dog.headers == {}
    assert dog.timeout == 30

def test_jobdog_custom_initialization():
    dog = JobDog(proxy="http://myproxy:8080", headers={"User-Agent": "MyBot"}, timeout=60)
    assert dog.proxy == "http://myproxy:8080"
    assert dog.headers == {"User-Agent": "MyBot"}
    assert dog.timeout == 60

def test_fetch_details_placeholder():
    dog = JobDog()
    result = dog.fetch_details("https://example.com/job/123")
    assert result == {"url": "https://example.com/job/123"}