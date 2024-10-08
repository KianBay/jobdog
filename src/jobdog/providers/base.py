from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def sanitize_url(self, url: str) -> str:
        pass

    @abstractmethod
    def parse_html(self, html: str) -> Dict[str, Any]:
        pass