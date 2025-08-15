"""
Configuration settings for Square OAuth integration.

Attributes:
    SCOPES (list): List of requested permissions for Square API access.
    SCOPE_STRING (str): Permissions joined as a '+' separated string for OAuth requests.
    REDIRECT_URI (str): Callback URI for OAuth authorization response.
    SESSION (bool): Indicates if session management is enabled.
    CODE_CHALLENGE_METHOD (str): Method used for PKCE code challenge.
    AUTH_URL (str): Base URL for Square OAuth authorization.
    POST_TOKEN_URL (str): URL for exchanging authorization code for access token.
    PORT (int): Port number for running the local application.
"""
import os
from dotenv import load_dotenv

load_dotenv()
SQUARE_APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID")
SQUARE_APPLICATION_SECRET = os.getenv("SQUARE_APPLICATION_SECRET")

# Requested permissions
SCOPES = [
    "CUSTOMERS_READ",
    "INVENTORY_READ",
    "ORDERS_READ",
    "PAYMENTS_READ"
]

# Authorization parameters
SCOPE_STRING = '+'.join(SCOPES)
REDIRECT_URI = "https://3d2c204044f7.ngrok-free.app/callback"
SESSION = False
CODE_CHALLENGE_METHOD = "S256"

# URLs
AUTH_URL = "https://connect.squareup.com/oauth2/authorize?"
POST_TOKEN_URL = "https://connect.squareup.com/oauth2/token"

PORT = 5000
