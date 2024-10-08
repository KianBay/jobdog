from urllib.parse import urlparse
from typing import Dict, Type
from .base import BaseParser
from ..exceptions import UnsupportedProviderError

PARSER_MAP: Dict[str, Type[BaseParser]] = {}

