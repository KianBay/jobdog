class JobDogException(Exception):
    """Base exception for JobDog"""


class JobDogSanitizeUrlError(JobDogException):
    """Raised when there's an error sanitizing the URL"""


class FetchError(JobDogException):
    """Raised when there's an error fetching job details"""


class ParserError(JobDogException):
    """Raised when there's an error parsing job details"""


class UnsupportedProviderError(JobDogException):
    """Raised when no parser is found for a given URL"""
