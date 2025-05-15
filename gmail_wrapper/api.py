"""
Gmail API interaction class using httpx.
"""

import asyncio
import base64
import email
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Literal

import httpx
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .consts import (
    CREDENTIALS_PATH,
    SCOPES,
    TOKEN_PATH,
    FLOW_PORT,
)

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
        Initializes the GmailAPICaller with a httpx.AsyncClient.
        """
        self._list_key: Literal["threads", "drafts", "messages"] = "threads"
        self._endpoint: Literal["threads", "drafts", "messages"] = "threads"
        self.credentials = self._get_credentials()
        self.base_url = "https://gmail.googleapis.com/gmail/v1/users/me"
        self.messages = []  # Placeholder for managing message states
        self.drafts = []  # Placeholder for managing draft states
        self.headers = self._get_headers()  # Initialize headers here
        self.client = self._get_client()

    def _get_client(self, proxy: bool = False):
        kwargs = {"headers": self.headers}
        if proxy:
            proxy_url = os.environ.get("HTTP_PROXY")
            if proxy_url:
                kwargs["proxies"] = {
                    "http://": proxy_url,
                    "https://": proxy_url,
                }

        client = httpx.AsyncClient(**kwargs)
        return client

    def _get_credentials(self) -> Credentials:  # noqa
        """
        Retrieves or refreshes Google API credentials.

        Returns:
            Credentials: The Google API credentials.
        """
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_PATH):
                    raise Exception(
                        f"Credentials file missing: {CREDENTIALS_PATH}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(
                    port=FLOW_PORT, redirect_uri_trailing_slash=False
                )
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return creds

    def _get_headers(self) -> dict[str, str]:
        """
        Creates the necessary headers for authenticated requests.

        Returns:
            dict[str, str]: The headers for authenticated requests.
        """
        access_token = self.credentials.token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # logger.debug(f"default headers are: {headers}")
        return headers

    def _flip_endpoint(
        self, endpoint: Literal["threads", "messages", "drafts"] | None = None
    ):
        """
        headers: dict[str, str] | None = None,

        :param endpoint: str
        :return:
            None
        """
        if not endpoint:
            if self._endpoint == "threads":
                self._endpoint = "messages"
            elif self._endpoint == "messages":
                self._endpoint = "drafts"
            elif self._endpoint == "drafts":
                self._endpoint = "threads"
        else:
            self._endpoint = endpoint

        self._list_key = self._endpoint

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Makes a request to the Gmail API.

        :param method: str
        :param endpoint: str
        :param params: dict[str, Any] | None
        :param data: dict[str, Any] | None
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = await self.client.get(
                    url, headers=request_headers, params=params
                )
            elif method == "POST":
                response = await self.client.post(
                    url, headers=request_headers, json=data
                )
            elif method == "PUT":
                response = await self.client.put(
                    url, headers=request_headers, json=data
                )
            elif method == "DELETE":
                response = await self.client.delete(
                    url, headers=request_headers
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error for {exc.request.url} -"
                f" {exc.response.status_code} - {exc.response.text}"
            )
            raise
        except httpx.RequestError as exc:
            logger.error(
                f"An error occurred while requesting {exc.request.url}."
            )
            raise

    async def get(
        self,
        resource_id: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Makes a GET request to the Gmail API.

        :param resource_id: str | None
        :param params: dict[str, Any] | None
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """
        endpoint = (
            f"{self._endpoint}/{resource_id}" if resource_id else self._endpoint
        )
        return await self._request(
            "GET", endpoint, params=params, headers=headers
        )

    async def get_all(
        self,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Makes a GET request to list resources from the Gmail API.

        :param params: dict[str, Any] | None
        :param headers: dict[str, str] | None
        :return:
            list[dict[str, Any]]
        """
        endpoint = self._endpoint
        response = await self._request(
            "GET", endpoint, params=params, headers=headers
        )
        logger.debug(f"Response: {response}")
        return response.get(self._list_key, [])

    async def create(
        self,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Makes a DELETE request to delete a resource in the Gmail API.

        :param data: dict[str, Any]
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """

        return await self._request(
            "POST", self._endpoint, data=data, headers=headers
        )

    async def delete(
        self,
        resource_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Makes a DELETE request to delete a resource in the Gmail API.

        :param resource_id: str
        :param headers: dict[str, str]| None
        :return:
            None
        """

        endpoint = f"{self._endpoint}/{resource_id}/trash"
        await self._request("DELETE", endpoint, headers=headers)

    async def undelete(
        self, resource_id: str, headers: dict[str, str] | None = None
    ):
        """
        Makes a POST request to undelete a resource in the Gmail API.

        :param resource_id:
        :param headers:
        :return:
        """
        endpoint = f"{self._endpoint}/{resource_id}/untrash"
        await self._request("POST", endpoint, headers=headers)

    async def update(
        self,
        resource_id: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Makes a PUT request to update a resource in the Gmail API.

        :param resource_id: str
        :param data: dict[str, Any]
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """

        endpoint = f"{self._endpoint}/{resource_id}"
        return await self._request("PUT", endpoint, data=data, headers=headers)

    async def close(self):
        """
        Closes the httpx.AsyncClient.
        """
        await self.client.aclose()

    async def create_message(  # noqa
        self,
        sender: str,
        to: str,
        subject: str,
        message_text: str,
        message_html: str | None = None,
        cc: list[str] | str | None = None,
    ) -> dict[str, str]:
        """
        Creates a message for an email.

        :param sender: str
        :param to: str
        :param subject: str
        :param message_text: str
        :param message_html: str = ''
        :param cc: str | list[str] | None = None
        :return:
        """
        message = MIMEMultipart("alternative")
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            message["Cc"] = cc

        # Handle Text and HTML alternatives.
        part1 = MIMEText(message_text, "plain")
        message.attach(part1)
        if message_html:
            part2 = MIMEText(message_html, "html")
            message.attach(part2)

        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    async def get_drafts(
        self, headers: dict[str, str] | None = None, details: bool = False
    ) -> list[dict[str, Any]]:
        """
        Retrieves a list of drafts from the Gmail API.

        :param headers: dict[str, str] | None
        :param details: bool
        :return:
            list[dict[str, str]]
        """

        if "drafts" not in self._endpoint:
            self._flip_endpoint("drafts")
        drafts = await self.get_all(headers=headers)
        if details:
            tasks = [
                asyncio.create_task(
                    self.get_draft(draft_id=draft.get("id"), headers=headers)
                )
                for draft in drafts
            ]
            drafts = await asyncio.gather(*tasks)
        return drafts

    async def get_draft(
        self, draft_id: str, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Retrieves a specific draft from the Gmail API.

        :param draft_id: str
        :param headers: dict[str, str] | None
        :return:
        """
        if "drafts" not in self._endpoint:
            self._flip_endpoint("drafts")
        return await self.get(
            draft_id, params={"format": "full"}, headers=headers
        )

    async def create_draft(
        self, message: dict[str, str], headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Creates a new draft in the Gmail API.

        :param message: dict[str, str]
        :param headers: dict[str, str] | None
        :return:
        """

        if "drafts" not in self._endpoint:
            self._flip_endpoint("drafts")
        self._endpoint = "drafts"
        return await self.create(data={"message": message}, headers=headers)

    async def send_message(
        self, message: dict[str, str], headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Sends an email message using the Gmail API.

        :param message: dict[str, str]
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """
        self._endpoint = "messages/send"
        return await self.create(data=message, headers=headers)

    async def get_messages(
        self, headers: dict[str, str] | None = None, details: bool = False
    ) -> list[dict[str, Any]]:
        """
        Retrieves a list of messages from the Gmail API.

        Returns:
            list[dict[str, Any]]: A list of message resources.
        """
        if "messages" not in self._endpoint:
            self._flip_endpoint("messages")
        messages = await self.get_all(headers=headers)
        if details:
            tasks = [
                asyncio.create_task(
                    self.get_message(
                        message_id=message.get("id"), headers=headers
                    )
                )
                for message in messages
            ]
            messages = await asyncio.gather(*tasks)
        return messages

    async def get_message(
        self, message_id: str, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Retrieves a specific message from the Gmail API.

        :param message_id: str
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """
        if "messages" not in self._endpoint:
            self._flip_endpoint("messages")
        self._endpoint = f"messages/{message_id}"
        return await self.get(
            message_id, params={"format": "full"}, headers=headers
        )

    async def delete_draft(
        self, draft_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Deletes a specific draft from the Gmail API.

        :param draft_id: str
        :param headers: dict[str, str] | None

        :return:
            None
        """
        if "drafts" not in self._endpoint:
            self._flip_endpoint("drafts")
        await self.delete(draft_id, headers=headers)

    async def delete_message(
        self, message_id: str, headers: dict[str, str] | None = None
    ) -> None:
        """
        Deletes a specific message from the Gmail API.

        Args:
            message_id (str): The ID of the message to delete.
        """
        self._endpoint = lambda resource_id: f"messages/{resource_id}"
        await self.delete(message_id, headers=headers)

    async def update_draft(
        self,
        draft_id: str,
        message: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Updates a specific draft in the Gmail API.

        :param draft_id: str
        :param message: dict[str, str]
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """
        if "drafts" not in self._endpoint:
            self._flip_endpoint("drafts")
        return await self.update(
            draft_id, data={"message": message}, headers=headers
        )

    async def update_message(
        self,
        message_id: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Updates a specific message in the Gmail API.

        :param message_id: str
        :param data: dict[str, Any]
        :param headers: dict[str, str] | None
        :return:
            dict[str, Any]
        """

        if "messages" not in self._endpoint:
            self._flip_endpoint("messages")
        return await self.update(message_id, data=data, headers=headers)

    def get_msg_from_str(  # noqa
        self, raw_content: str
    ) -> email.message.Message:  # noqa
        """
        Get message from string.

        Args:
            raw_content: Raw content of the message.

        Returns:
            Message object.
        """
        raw_content = raw_content.replace("_", "/").replace("-", "+")

        email_msg = base64.urlsafe_b64decode(
            raw_content.encode("ASCII")
        ).decode("ASCII")
        return email.message_from_string(email_msg)


gmail_service = GmailAPICaller()
