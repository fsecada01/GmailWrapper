"""
Gmail drafts resource.
"""

from typing import Any

from .base import BaseGmailResource


class GmailDrafts(BaseGmailResource):
    """Handles Gmail draft operations."""

    async def get_all(
        self,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        details: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Get all drafts.

        Args:
            params: Query parameters
            headers: Additional headers
            details: Whether to get full draft details

        Returns:
            list[dict[str, Any]]: List of drafts
        """
        if details:
            return await self.get_all_with_details(
                self.config.DRAFTS_ENDPOINT,
                "drafts",
                self.get_by_id,
                params=params,
                headers=headers,
            )
        else:
            return await super().get_all(
                self.config.DRAFTS_ENDPOINT,
                "drafts",
                params=params,
                headers=headers,
            )

    async def get_by_id(
        self,
        draft_id: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Get a specific draft by ID.

        Args:
            draft_id: Draft ID
            headers: Additional headers

        Returns:
            dict[str, Any]: Draft data
        """
        params = {"format": self.config.FULL_FORMAT}
        return await super().get_by_id(
            self.config.DRAFTS_ENDPOINT,
            draft_id,
            params=params,
            headers=headers,
        )

    async def create(
        self,
        message: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new draft.

        Args:
            message: Draft message data
            headers: Additional headers

        Returns:
            dict[str, Any]: Created draft data
        """
        return await super().create(
            self.config.DRAFTS_ENDPOINT,
            data={"message": message},
            headers=headers,
        )

    async def update(
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
        return await super().update(
            self.config.DRAFTS_ENDPOINT,
            draft_id,
            data={"message": message},
            headers=headers,
        )

    async def delete(
        self,
        draft_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Delete a draft.

        Args:
            draft_id: Draft ID
            headers: Additional headers
        """
        await super().delete(
            self.config.DRAFTS_ENDPOINT, draft_id, headers=headers
        )
