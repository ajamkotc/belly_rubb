"""
This class provides functionality for retrieving, validating, refreshing, and updating
OAuth access tokens in the database. It interacts with an OAuth API client and the
database to ensure that merchants have valid access tokens for authentication.
from the database. 

    Raises InvalidTokenException if no valid token is found.
    Checks whether the provided access token has expired. Raises InvalidTokenException
        if the token is None or invalid.
    Raises InvalidTokenException if the token is None or invalid.
    Updates the access token in the database with new token information and returns
        the updated AccessToken instance.
    Refreshes the access token using the refresh token if possible. Raises
    InvalidTokenException if the token is None, invalid, or cannot be refreshed.
    Retrieves a valid access token for the specified merchant, refreshing it if
        necessary. Returns the access token string.
"""
from datetime import datetime, timezone
from dateutil import parser
import requests
from sqlalchemy import select, update
from loguru import logger

from app.exceptions import InvalidTokenException
from app.db_models import AccessToken
from app.db import Session
from app.config import POST_TOKEN_URL, SQUARE_APPLICATION_ID

class TokenProvider:
    """
    TokenProvider is responsible for managing OAuth access tokens for merchants.
    
    Functionality includes access token retrieval, validation, refreshing,
    and updating tokens in the database.
        
    Methods:
        _pull_token(merchant_id: str, session) -> AccessToken:
            Retrieves the most recently created access token for the specified merchant
            from the database.
        _is_expired(token: AccessToken) -> bool:
            Checks whether the provided access token has expired.
        _can_refresh(token: AccessToken) -> bool:
            Checks whether the provided access token can be refreshed using its refresh token.
        _update_token(token_info: dict, merchant_id: str) -> AccessToken:
            Updates the access token in the database with new token information.
        _refresh_token(token: AccessToken, merchant_id: str) -> AccessToken:
            Refreshes the access token using the refresh token if possible.
        get_access_token(merchant_id: str) -> str:
            Retrieves a valid access token for the specified merchant, refreshing it if necessary.
    """
    def _pull_token(self, merchant_id: str, session) -> AccessToken:
        """
        Retrieves the most recently created access token for the specified merchant.

        Args:
            merchant_id (str): The unique identifier of the merchant.
            session: The database session to use for the query.

        Returns:
            AccessToken: The access token associated with the merchant.

        Raises:
            InvalidTokenException: If no valid token is found for the given merchant.
        """
        stmt = (
            select(AccessToken)
            .where(AccessToken.merchant_id == merchant_id)
            .order_by(AccessToken.created_at.desc())
        )

        token = session.execute(stmt).scalars().first()

        if not token:
            raise InvalidTokenException("No valid token found.")

        return token

    def _is_expired(self, token: AccessToken) -> bool:
        """
        Checks whether the provided access token has expired.

        Args:
            token (AccessToken): The access token to check.

        Raises:
            InvalidTokenException: If the token is None or invalid.

        Returns:
            bool: True if the token has expired, False otherwise.
        """
        if not token:
            raise InvalidTokenException("No valid token found.")

        return parser.isoparse(token.expires_at) <= datetime.now(timezone.utc)

    def _can_refresh(self, token: AccessToken) -> bool:
        """
        Checks whether the provided access token can be refreshed using its refresh token.

        Args:
            token (AccessToken): The access token to check.

        Raises:
            InvalidTokenException: If the token is None or invalid.

        Returns:
            bool: True if the refresh token is still valid, False otherwise.
        """
        if not token:
            raise InvalidTokenException("No valid token found.")

        return parser.isoparse(token.refresh_token_expires_at) > datetime.now(timezone.utc)

    def _update_token(self, token_info: dict, merchant_id: str, session) -> None:
        """
        Updates the access token in the database.

        Args:
            token_info (dict): A dictionary containing the updated token information.
            merchant_id (str): The unique identifier of the merchant.
            session: The database session to use for the update.

        Returns:
            token (AccessToken): The updated access token.
        """
        stmt = (
            update(AccessToken)
            .where(AccessToken.merchant_id == merchant_id)
            .values(
                merchant_id=merchant_id,
                access_token=token_info.get("access_token"),
                token_type=token_info.get("token_type"),
                expires_at=parser.isoparse(token_info.get("expires_at")),
                refresh_token=token_info.get("refresh_token"),
                short_lived=token_info.get("short_lived", False),
                refresh_token_expires_at=parser.isoparse(
                    token_info.get("refresh_token_expires_at"))
            )
        )

        session.execute(stmt)

    def _refresh_token(self, token: AccessToken, merchant_id: str, session) -> AccessToken:
        """
        Refreshes the access token using the refresh token.

        Args:
            token (AccessToken): The access token to refresh.
            merchant_id (str): The unique identifier of the merchant.
            session: The database session to use for the refresh request.

        Raises:
            InvalidTokenException: If the token is None or invalid.
        """
        # Check if token is valid
        if not token:
            raise InvalidTokenException("No valid token found.")

        # Check if can use refresh token
        if self._can_refresh(token):
            logger.info("Refreshing access token using refresh token.")
            print(token.refresh_token)
            # Make API request to refresh token
            response = requests.post(
                POST_TOKEN_URL,
                headers={
                    'Content-Type': 'application/json'
                },
                json={
                   'client_id': SQUARE_APPLICATION_ID,
                   'refresh_token': token.refresh_token,
                   'grant_type': 'refresh_token'
                },
                timeout=30
            )
            print(response.json())
            return self._update_token(response.json(), merchant_id, session)

        logger.error("Failed to refresh access token, please re-authenticate with /auth.")
        raise InvalidTokenException("Failed to refresh access token.")

    def get_access_token(self, merchant_id: str) -> str:
        """
        Retrieves the access token for the current user.

        Args:
            merchant_id (str): The unique identifier of the merchant.

        Returns:
            str: The access token for the current user.
        """
        with Session() as session:
            with session.begin():
                # Get the most recent access token for the merchant
                token = self._pull_token(merchant_id, session)

                # Check if token is expired
                if self._is_expired(token):
                    # Try to refresh token
                    self._refresh_token(token, merchant_id, session)

                    # Get new token
                    token = self._pull_token(merchant_id, session)

                access_token = token.access_token

            return access_token
