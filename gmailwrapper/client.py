"""
HTTP client for Gmail API interactions.
"""

import os
from typing import Any

import httpx

from .auth import GmailAuthenticator
from .exceptions import GmailAPIError, GmailRequestError

try:
    from backend.logger import logger
except ImportError:
    from loguru import logger


class GmailHTTPClient:
    """Handles HTTP requests to Gmail API."""

    def __init__(self, authenticator: GmailAuthenticator, base_url: str):
        """
        Initialize the HTTP client.

        Args:
            authenticator: Gmail authenticator instance
            base_url: Base URL for Gmail API
        """
        self.authenticator = authenticator
        self.base_url = base_url
        self._client = None

    def _get_client(self, proxy: bool = False) -> httpx.AsyncClient:
        """Get or create httpx client."""
        if self._client is None:
            headers = self.authenticator.get_auth_headers()
            kwargs = {"headers": headers}

            if proxy:
                proxy_url = os.environ.get("HTTP_PROXY")
                if proxy_url:
                    kwargs["proxies"] = {
                        "http://": proxy_url,
                        "https://": proxy_url,
                    }

            self._client = httpx.AsyncClient(**kwargs)
        return self._client

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Make a request to the Gmail API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: JSON data for request body
            headers: Additional headers

        Returns:
            dict[str, Any]: API response data

        Raises:
            GmailAPIError: When API returns an error
            GmailRequestError: When HTTP request fails
        """
        client = self._get_client()
        request_headers = self.authenticator.get_auth_headers().copy()

        if headers:
            request_headers.update(headers)

        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = await client.get(
                    url, headers=request_headers, params=params
                )
            elif method == "POST":
                response = await client.post(
                    url, headers=request_headers, json=data
                )
            elif method == "PUT":
                response = await client.put(
                    url, headers=request_headers, json=data
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as exc:
            error_msg = (
                f"HTTP error for {exc.request.url} - "
                f"{exc.response.status_code} - {exc.response.text}"
            )
            logger.error(error_msg)
            raise GmailAPIError(
                error_msg,
                status_code=exc.response.status_code,
                response=exc.response.text,
            )
        except httpx.RequestError as exc:
            error_msg = f"Request error for {exc.request.url}: {exc}"
            logger.error(error_msg)
            raise GmailRequestError(error_msg)

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request."""
        return await self.request(
            "GET", endpoint, params=params, headers=headers
        )

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, data=data, headers=headers)

    async def put(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, data=data, headers=headers)

    async def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Make a DELETE request."""
        await self.request("DELETE", endpoint, headers=headers)

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
