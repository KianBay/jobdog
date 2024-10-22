from urllib.parse import urlparse
from typing import Type
from jobdog.exceptions import UnsupportedProviderError
from jobdog.providers.base import BaseParser

PARSER_MAP: dict[str, Type[BaseParser]] = {}


def register_parser(domain: str):
    def decorator(cls):
        PARSER_MAP[domain] = cls
        return cls

    return decorator


def get_parser(url: str) -> BaseParser:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    main_domain = ".".join(domain.split(".")[-2:])

    parser_class = PARSER_MAP.get(main_domain)
    if parser_class is None:
        raise UnsupportedProviderError(f"No parser found for domain: {main_domain}")
    return parser_class()
