"""
Configuration for Gmail Wrapper.
"""

from dataclasses import dataclass


@dataclass
class GmailConfig:
    """Gmail API configuration."""

    BASE_URL: str = "https://gmail.googleapis.com/gmail/v1/users/me"

    # Endpoints
    MESSAGES_ENDPOINT: str = "messages"
    DRAFTS_ENDPOINT: str = "drafts"
    THREADS_ENDPOINT: str = "threads"
    SEND_ENDPOINT: str = "messages/send"

    # Operations
    TRASH_SUFFIX: str = "trash"
    UNTRASH_SUFFIX: str = "untrash"

    # Request formats
    FULL_FORMAT: str = "full"
