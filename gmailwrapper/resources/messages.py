"""
Gmail messages resource.
"""

import base64
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from .base import BaseGmailResource


class GmailMessages(BaseGmailResource):
    """Handles Gmail message operations."""

    async def get_all(
        self,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        details: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Get all messages.

        Args:
            params: Query parameters
            headers: Additional headers
            details: Whether to get full message details

        Returns:
            list[dict[str, Any]]: List of messages
        """
        if details:
            return await self.get_all_with_details(
                self.config.MESSAGES_ENDPOINT,
                "messages",
                self.get_by_id,
                params=params,
                headers=headers,
            )
        else:
            return await super().get_all(
                self.config.MESSAGES_ENDPOINT,
                "messages",
                params=params,
                headers=headers,
            )

    async def get_by_id(
        self,
        message_id: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: Message ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Message data
        """
        params = {"format": self.config.FULL_FORMAT}
        return await super().get_by_id(
            self.config.MESSAGES_ENDPOINT,
            message_id,
            params=params,
            headers=headers,
        )

    async def send(
        self,
        message: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Send a message.

        Args:
            message: Message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Sent message data
        """
        return await self.create(
            self.config.SEND_ENDPOINT, data=message, headers=headers
        )

    async def delete(
        self,
        message_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Delete a message.

        Args:
            message_id: Message ID
            headers: Additional headers
        """
        await super().delete(
            self.config.MESSAGES_ENDPOINT, message_id, headers=headers
        )

    async def update(
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
        return await super().update(
            self.config.MESSAGES_ENDPOINT,
            message_id,
            data=data,
            headers=headers,
        )

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
        Create a message for sending.

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
        message = MIMEMultipart("alternative")
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject

        if cc:
            if isinstance(cc, str):
                cc = [cc]
            message["Cc"] = ", ".join(cc)

        part1 = MIMEText(message_text, "plain")
        message.attach(part1)

        if message_html:
            part2 = MIMEText(message_html, "html")
            message.attach(part2)

        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def parse_message(self, raw_content: str) -> email.message.Message:
        """
        Parse raw message content.

        Args:
            raw_content: Raw message content

        Returns:
            email.message.Message: Parsed message object
        """
        raw_content = raw_content.replace("_", "/").replace("-", "+")
        email_msg = base64.urlsafe_b64decode(
            raw_content.encode("ASCII")
        ).decode("ASCII")
        return email.message_from_string(email_msg)
