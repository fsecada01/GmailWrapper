"""
Base class for Gmail resources.
"""

import asyncio
from typing import Any

from ..client import GmailHTTPClient
from ..config import GmailConfig
from ..exceptions import GmailResourceError

try:
    from backend.logger import logger
except ImportError:
    from loguru import logger


class BaseGmailResource:
    """Base class for Gmail resource operations."""

    def __init__(self, client: GmailHTTPClient, config: GmailConfig):
        """
        Initialize the resource.

        Args:
            client: HTTP client instance
            config: Gmail configuration
        """
        self.client = client
        self.config = config

    async def get_all(
        self,
        endpoint: str,
        list_key: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all resources of a type.

        Args:
            endpoint: API endpoint
            list_key: Key for list in response
            params: Query parameters
            headers: Additional headers

        Returns:
            list[dict[str, Any]]: List of resources
        """
        try:
            response = await self.client.get(
                endpoint, params=params, headers=headers
            )
            return response.get(list_key, [])
        except Exception as e:
            raise GmailResourceError(f"Failed to get {endpoint}: {e}")

    async def get_by_id(
        self,
        endpoint: str,
        resource_id: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Get a specific resource by ID.

        Args:
            endpoint: API endpoint
            resource_id: Resource ID
            params: Query parameters
            headers: Additional headers

        Returns:
            dict[str, Any]: Resource data
        """
        try:
            full_endpoint = f"{endpoint}/{resource_id}"
            return await self.client.get(
                full_endpoint, params=params, headers=headers
            )
        except Exception as e:
            raise GmailResourceError(
                f"Failed to get {endpoint}/{resource_id}: {e}"
            )

    async def create(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new resource.

        Args:
            endpoint: API endpoint
            data: Resource data
            headers: Additional headers

        Returns:
            dict[str, Any]: Created resource data
        """
        try:
            return await self.client.post(endpoint, data=data, headers=headers)
        except Exception as e:
            raise GmailResourceError(f"Failed to create {endpoint}: {e}")

    async def update(
        self,
        endpoint: str,
        resource_id: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Update a resource.

        Args:
            endpoint: API endpoint
            resource_id: Resource ID
            data: Updated resource data
            headers: Additional headers

        Returns:
            dict[str, Any]: Updated resource data
        """
        try:
            full_endpoint = f"{endpoint}/{resource_id}"
            return await self.client.put(
                full_endpoint, data=data, headers=headers
            )
        except Exception as e:
            raise GmailResourceError(
                f"Failed to update {endpoint}/{resource_id}: {e}"
            )

    async def delete(
        self,
        endpoint: str,
        resource_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Delete a resource.

        Args:
            endpoint: API endpoint
            resource_id: Resource ID
            headers: Additional headers
        """
        try:
            full_endpoint = (
                f"{endpoint}/{resource_id}/{self.config.TRASH_SUFFIX}"
            )
            await self.client.delete(full_endpoint, headers=headers)
        except Exception as e:
            raise GmailResourceError(
                f"Failed to delete {endpoint}/{resource_id}: {e}"
            )

    async def undelete(
        self,
        endpoint: str,
        resource_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Undelete a resource.

        Args:
            endpoint: API endpoint
            resource_id: Resource ID
            headers: Additional headers
        """
        try:
            full_endpoint = (
                f"{endpoint}/{resource_id}/{self.config.UNTRASH_SUFFIX}"
            )
            await self.client.post(full_endpoint, data={}, headers=headers)
        except Exception as e:
            raise GmailResourceError(
                f"Failed to undelete {endpoint}/{resource_id}: {e}"
            )

    async def get_all_with_details(
        self,
        endpoint: str,
        list_key: str,
        get_detail_func,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all resources with full details.

        Args:
            endpoint: API endpoint
            list_key: Key for list in response
            get_detail_func: Function to get detailed resource
            params: Query parameters
            headers: Additional headers

        Returns:
            list[dict[str, Any]]: List of detailed resources
        """
        resources = await self.get_all(
            endpoint, list_key, params=params, headers=headers
        )

        if not resources:
            return []

        tasks = [
            asyncio.create_task(
                get_detail_func(resource.get("id"), headers=headers)
            )
            for resource in resources
        ]
        return await asyncio.gather(*tasks)
