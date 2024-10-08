from urllib.parse import urlparse
from typing import Dict, Type
from .base import BaseParser
from ..exceptions import UnsupportedProviderError

PARSER_MAP: Dict[str, Type[BaseParser]] = {}

def register_parser(domain: str):
    def decorator(cls):
        PARSER_MAP[domain] = cls
        return cls
    return decorator

def get_parser(url: str) -> BaseParser:
    domain = urlparse(url).netloc
    parser_class = PARSER_MAP.get(domain)
    if parser_class is None:
        raise UnsupportedProviderError(f"No parser found for domain: {domain}")
    return parser_class()