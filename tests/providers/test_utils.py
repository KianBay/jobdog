import pytest
from jobdog.providers.base import BaseParser
from jobdog.providers.utils import register_parser, get_parser, PARSER_MAP
from jobdog.exceptions import UnsupportedProviderError


def test_base_parser_is_abstract():
    with pytest.raises(TypeError):
        BaseParser()


def test_register_and_get_parser():
    PARSER_MAP.clear()

    @register_parser("example.com")
    class ExampleParser(BaseParser):
        def sanitize_url(self, url):
            return url

        def parse_html(self, html):
            return {"title": "Example Job"}


    assert "example.com" in PARSER_MAP


    parser = get_parser("https://example.com/job/123")
    assert isinstance(parser, ExampleParser)


    with pytest.raises(UnsupportedProviderError):
        get_parser("https://unknown.com/job/123")


def test_multiple_parser_registration():
    PARSER_MAP.clear()

    @register_parser("site1.com")
    class Site1Parser(BaseParser):
        def sanitize_url(self, url):
            return url

        def parse_html(self, html):
            return {"title": "Site1 Job"}

    @register_parser("site2.com")
    class Site2Parser(BaseParser):
        def sanitize_url(self, url):
            return url

        def parse_html(self, html):
            return {"title": "Site2 Job"}

    assert "site1.com" in PARSER_MAP
    assert "site2.com" in PARSER_MAP
    assert isinstance(get_parser("https://site1.com/job/123"), Site1Parser)
    assert isinstance(get_parser("https://site2.com/job/456"), Site2Parser)