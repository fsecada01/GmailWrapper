"""
Gmail API interaction class using httpx.
"""

import email
from typing import Any

from .auth import GmailAuthenticator
from .client import GmailHTTPClient
from .config import GmailConfig
from .resources import GmailMessages, GmailDrafts, GmailThreads

try:
    from backend.logger import logger
except ImportError:
    from loguru import logger


class GmailAPICaller:
    """
    A class to interact with the Gmail API using httpx.
    """

    def __init__(self):
        """
        Initialize the Gmail API caller with modular components.
        """
        self.config = GmailConfig()
        self.authenticator = GmailAuthenticator()
        self.client = GmailHTTPClient(self.authenticator, self.config.BASE_URL)

        # Resource handlers
        self.messages = GmailMessages(self.client, self.config)
        self.drafts = GmailDrafts(self.client, self.config)
        self.threads = GmailThreads(self.client, self.config)

    async def close(self):
        """
        Close the HTTP client.
        """
        await self.client.close()

    def create_message(
        self,
        sender: str,
        to: str,
        subject: str,
        message_text: str,
        message_html: str | None = None,
        cc: list[str] | str | None = None,
    ) -> dict[str, str]:
        """
        Create a message for an email.

        Args:
            sender: Sender email
            to: Recipient email
            subject: Email subject
            message_text: Plain text content
            message_html: HTML content
            cc: CC recipients

        Returns:
            dict[str, str]: Message data ready for sending
        """
        return self.messages.create_message(
            sender, to, subject, message_text, message_html, cc
        )

    async def get_drafts(
        self, headers: dict[str, str] | None = None, details: bool = False
    ) -> list[dict[str, Any]]:
        """
        Get all drafts.

        Args:
            headers: Additional headers
            details: Whether to get full draft details

        Returns:
            list[dict[str, Any]]: List of drafts
        """
        return await self.drafts.get_all(headers=headers, details=details)

    async def get_draft(
        self, draft_id: str, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Get a specific draft by ID.

        Args:
            draft_id: Draft ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Draft data
        """
        return await self.drafts.get_by_id(draft_id, headers=headers)

    async def create_draft(
        self, message: dict[str, str], headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Create a new draft.

        Args:
            message: Draft message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Created draft data
        """
        return await self.drafts.create(message, headers=headers)

    async def send_message(
        self, message: dict[str, str], headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Send an email message.

        Args:
            message: Message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Sent message data
        """
        return await self.messages.send(message, headers=headers)

    async def get_messages(
        self, headers: dict[str, str] | None = None, details: bool = False
    ) -> list[dict[str, Any]]:
        """
        Get all messages.

        Args:
            headers: Additional headers
            details: Whether to get full message details

        Returns:
            list[dict[str, Any]]: List of messages
        """
        return await self.messages.get_all(headers=headers, details=details)

    async def get_message(
        self, message_id: str, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: Message ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Message data
        """
        return await self.messages.get_by_id(message_id, headers=headers)

    async def delete_draft(
        self, draft_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Delete a draft.

        Args:
            draft_id: Draft ID
            headers: Additional headers
        """
        await self.drafts.delete(draft_id, headers=headers)

    async def delete_message(
        self, message_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Delete a message.

        Args:
            message_id: Message ID
            headers: Additional headers
        """
        await self.messages.delete(message_id, headers=headers)

    async def update_draft(
        self,
        draft_id: str,
        message: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Update a draft.

        Args:
            draft_id: Draft ID
            message: Updated draft message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Updated draft data
        """
        return await self.drafts.update(draft_id, message, headers=headers)

    async def update_message(
        self,
        message_id: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Update a message.

        Args:
            message_id: Message ID
            data: Updated message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Updated message data
        """
        return await self.messages.update(message_id, data, headers=headers)

    def get_msg_from_str(self, raw_content: str) -> email.message.Message:
        """
        Parse raw message content.

        Args:
            raw_content: Raw message content

        Returns:
            email.message.Message: Parsed message object
        """
        return self.messages.parse_message(raw_content)

    # Thread methods
    async def get_threads(
        self, headers: dict[str, str] | None = None, details: bool = False
    ) -> list[dict[str, Any]]:
        """
        Get all threads.

        Args:
            headers: Additional headers
            details: Whether to get full thread details

        Returns:
            list[dict[str, Any]]: List of threads
        """
        return await self.threads.get_all(headers=headers, details=details)

    async def get_thread(
        self, thread_id: str, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Get a specific thread by ID.

        Args:
            thread_id: Thread ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Thread data
        """
        return await self.threads.get_by_id(thread_id, headers=headers)

    async def delete_thread(
        self, thread_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Delete a thread.

        Args:
            thread_id: Thread ID
            headers: Additional headers
        """
        await self.threads.delete(thread_id, headers=headers)

    async def undelete_thread(
        self, thread_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Undelete a thread.

        Args:
            thread_id: Thread ID
            headers: Additional headers
        """
        await self.threads.undelete(thread_id, headers=headers)


gmail_service = GmailAPICaller()
