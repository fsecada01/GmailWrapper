"""Gmail Wrapper - A Python module for interacting with the Gmail API."""

from .api import GmailAPICaller, gmail_service
from .auth import GmailAuthenticator
from .client import GmailHTTPClient
from .config import GmailConfig
from .exceptions import (
    GmailWrapperError,
    GmailAuthError,
    GmailCredentialsError,
    GmailTokenError,
    GmailAPIError,
    GmailRequestError,
    GmailResourceError,
)
from .resources import GmailMessages, GmailDrafts, GmailThreads

__version__ = "1.0.0b0"

# For backwards compatibility
GmailWrapper = GmailAPICaller

__all__ = [
    "GmailAPICaller",
    "GmailWrapper",  # backwards compatibility
    "gmail_service",
    "GmailAuthenticator",
    "GmailHTTPClient",
    "GmailConfig",
    "GmailMessages",
    "GmailDrafts",
    "GmailThreads",
    "GmailWrapperError",
    "GmailAuthError",
    "GmailCredentialsError",
    "GmailTokenError",
    "GmailAPIError",
    "GmailRequestError",
    "GmailResourceError",
]
