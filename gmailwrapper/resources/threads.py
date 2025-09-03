"""
Gmail threads resource.
"""

from typing import Any

from .base import BaseGmailResource


class GmailThreads(BaseGmailResource):
    """Handles Gmail thread operations."""

    async def get_all(
        self,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        details: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Get all threads.

        Args:
            params: Query parameters
            headers: Additional headers
            details: Whether to get full thread details

        Returns:
            list[dict[str, Any]]: List of threads
        """
        if details:
            return await self.get_all_with_details(
                self.config.THREADS_ENDPOINT,
                "threads",
                self.get_by_id,
                params=params,
                headers=headers,
            )
        else:
            return await super().get_all(
                self.config.THREADS_ENDPOINT,
                "threads",
                params=params,
                headers=headers,
            )

    async def get_by_id(
        self,
        thread_id: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Get a specific thread by ID.

        Args:
            thread_id: Thread ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Thread data
        """
        params = {"format": self.config.FULL_FORMAT}
        return await super().get_by_id(
            self.config.THREADS_ENDPOINT,
            thread_id,
            params=params,
            headers=headers,
        )

    async def delete(
        self,
        thread_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Delete a thread.

        Args:
            thread_id: Thread ID
            headers: Additional headers
        """
        await super().delete(
            self.config.THREADS_ENDPOINT, thread_id, headers=headers
        )

    async def undelete(
        self,
        thread_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Undelete a thread.

        Args:
            thread_id: Thread ID
            headers: Additional headers
        """
        await super().undelete(
            self.config.THREADS_ENDPOINT, thread_id, headers=headers
        )
