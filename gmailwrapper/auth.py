"""
Gmail authentication handler.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .consts import CREDENTIALS_PATH, SCOPES, TOKEN_PATH, FLOW_PORT
from .exceptions import GmailCredentialsError, GmailTokenError

try:
    from backend.logger import logger
except ImportError:
    from loguru import logger


class GmailAuthenticator:
    """Handles Gmail OAuth authentication and token management."""

    def __init__(self):
        """Initialize the authenticator."""
        self._credentials = None

    def get_credentials(self) -> Credentials:
        """
        Retrieves or refreshes Google API credentials.

        Returns:
            Credentials: The Google API credentials.

        Raises:
            GmailCredentialsError: When credentials file is missing.
            GmailTokenError: When token refresh fails.
        """
        if self._credentials and self._credentials.valid:
            return self._credentials

        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    raise GmailTokenError(f"Failed to refresh token: {e}")
            else:
                creds = self._get_new_credentials()

            self._save_token(creds)

        self._credentials = creds
        return creds

    def _get_new_credentials(self) -> Credentials:
        """Get new credentials via OAuth flow."""
        if not os.path.exists(CREDENTIALS_PATH):
            raise GmailCredentialsError(
                f"Credentials file missing: {CREDENTIALS_PATH}"
            )

        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            return flow.run_local_server(
                port=FLOW_PORT, redirect_uri_trailing_slash=False
            )
        except Exception as e:
            raise GmailCredentialsError(f"OAuth flow failed: {e}")

    def _save_token(self, credentials: Credentials) -> None:
        """Save credentials to token file."""
        try:
            with open(TOKEN_PATH, "w") as token:
                token.write(credentials.to_json())
        except Exception as e:
            logger.warning(f"Failed to save token: {e}")

    def get_auth_headers(self) -> dict[str, str]:
        """
        Get authorization headers for API requests.

        Returns:
            dict[str, str]: Headers with authorization token.
        """
        credentials = self.get_credentials()
        return {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }
