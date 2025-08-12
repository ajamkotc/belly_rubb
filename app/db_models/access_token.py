"""
SQLAlchemy ORM model for the 'access_tokens' table.

Classes:
    User: Represents an access token record associated with a merchant.

Attributes:
    merchant_id (str): Primary key, unique identifier for the merchant.
    access_token (str): The access token string.
    token_type (str): The type of the access token.
    expires_at (datetime): Expiration datetime of the access token.
    refresh_token (str): The refresh token string.
    short_lived (bool): Indicates if the token is short-lived. Defaults to False.
    refresh_token_expires_at (datetime): Expiration datetime of the refresh token.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from app.db import Base

class AccessToken(Base):
    """
    Represents an access token for a merchant.

    Attributes:
        merchant_id (str): The unique identifier for the merchant. Primary key.
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., Bearer).
        expires_at (datetime): The expiration datetime of the access token.
        refresh_token (str): The refresh token string.
        short_lived (bool): Indicates if the token is short-lived. Defaults to False.
        refresh_token_expires_at (datetime): The expiration datetime of the refresh token.
        created_at (datetime): The datetime when the token was created.
            Defaults to current UTC time.
    """
    __tablename__ = 'access_tokens'

    merchant_id = Column(String, primary_key=True)
    access_token = Column(String)
    token_type = Column(String)
    expires_at = Column(DateTime)
    refresh_token = Column(String)
    short_lived = Column(Boolean, default=False)
    refresh_token_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<AccessToken(merchant_id={self.merchant_id}, access_token={self.access_token})>"
