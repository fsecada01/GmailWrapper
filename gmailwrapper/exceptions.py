"""
Custom exceptions for the Gmail Wrapper.
"""


class GmailWrapperError(Exception):
    """Base exception for all Gmail Wrapper errors."""

    pass


class GmailAuthError(GmailWrapperError):
    """Raised when authentication fails."""

    pass


class GmailCredentialsError(GmailAuthError):
    """Raised when credentials are missing or invalid."""

    pass


class GmailTokenError(GmailAuthError):
    """Raised when token refresh fails."""

    pass


class GmailAPIError(GmailWrapperError):
    """Raised when Gmail API returns an error."""

    def __init__(
        self, message: str, status_code: int = None, response: str = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class GmailRequestError(GmailWrapperError):
    """Raised when HTTP request fails."""

    pass


class GmailResourceError(GmailWrapperError):
    """Raised when resource operations fail."""

    pass
