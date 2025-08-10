"""
This module implements the OAuth 2.0 PKCE flow for authenticating users with Square's API.

This generates a secure authentication flow in a Flask web application and provides routes for 
initiating the OAuth flow, handling the callback, and storing access tokens securely in a database.

Main Features:
- Home route to render the landing page.
- PKCE code challenge generation using SHA-256 and Base64 encoding.
- OAuth authorization route that generates CSRF tokens and code verifiers.
- Callback route to handle authorization server responses, verify CSRF state, 
    and exchange authorization codes for access tokens.
- Secure storage of token information in a database.
- Database initialization and Flask app startup.

Dependencies:
- Flask for web routing and session management.
- Requests for HTTP requests to the OAuth server.
- SQLAlchemy for database operations.
- dotenv for environment variable management.
- Square API configuration constants.

Usage:
Run this module to start the Flask application
    and expose endpoints for OAuth authentication with Square.
"""
import os
import secrets
import hashlib
import base64
import requests
from flask import Flask, render_template, session, redirect, request
from dotenv import load_dotenv
from dateutil import parser
from loguru import logger

from app.config import SCOPE_STRING, AUTH_URL, SESSION, POST_TOKEN_URL, REDIRECT_URI, \
    CODE_CHALLENGE_METHOD, PORT
from app.db import Session, init_db
from app.db_models import AccessToken

load_dotenv()
APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID")
APPLICATION_SECRET = os.getenv("SQUARE_APPLICATION_SECRET")

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

@app.route('/')
def home():
    """
    Render the home page with a link to initiate the OAuth flow.
    """
    return render_template('home.html')

def generate_code_challenge(code_verifier: str) -> str:
    """
    Generates a PKCE code challenge from a given code verifier.

    This function applies the SHA-256 hash algorithm to the provided code verifier,
    then encodes the result using URL-safe Base64 encoding, removing any trailing '='
    characters as specified by the PKCE specification.

    Args:
        code_verifier (str): The code verifier string to be transformed into a code challenge.

    Returns:
        str: The resulting code challenge string, suitable for use in OAuth 2.0 PKCE flows.
    """

    code_hash = hashlib.sha256(code_verifier.encode()).digest()
    encoded_hash = base64.urlsafe_b64encode(code_hash).rstrip(b'=')

    return encoded_hash.decode()

@app.route('/auth')
def auth():
    """
    Initiates the OAuth 2.0 authorization flow.

    Generates a CSRF token and stores it in the session.
    Generates a code verifier and generates code challenge to pass in
    authorization URL.
    Redirects the user to the authorization URL.

    Returns:
        redirect: Redirects to the Square OAuth authorization URL.
    """
    # Generate CSRF Token
    state = secrets.token_urlsafe(16)
    session['state'] = state
    logger.debug(f"Generated CSRF state: {state}")

    # Code verifier
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier
    logger.debug(f"Generated code verifier: {code_verifier}")

    # Generate authorization url
    auth_url = (
        AUTH_URL +
        f"client_id={APPLICATION_ID}"
        f"&scope={SCOPE_STRING}"
        f"&session={SESSION}"
        f"&state={state}"
        f"&code_challenge={generate_code_challenge(code_verifier)}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&code_challenge_method={CODE_CHALLENGE_METHOD}"
    )
    logger.debug(f"Generated authorization URL: {auth_url}")
    return redirect(auth_url)

def store_token_info(token_info: dict) -> None:
    """
    Stores the access token information in the database.

    Args:
        token_info (dict): The token information returned from the OAuth server.
    """
    session_db = Session()
    access_token = AccessToken(
        merchant_id=token_info['merchant_id'],
        access_token=token_info['access_token'],
        token_type=token_info['token_type'],
        expires_at=parser.isoparse(token_info['expires_at']),
        refresh_token=token_info.get('refresh_token'),
        short_lived=token_info.get('short_lived', False),
        refresh_token_expires_at=parser.isoparse(
            token_info.get('refresh_token_expires_at', 0))
    )

    logger.debug(f"Storing token info: {access_token}")

    session_db.add(access_token)
    session_db.commit()
    session_db.close()

    logger.success("Token information stored successfully.")

@app.route('/callback')
def callback():
    """
    Handles the OAuth 2.0 callback from the authorization server.

    Verifies the CSRF state parameter and exchanges the authorization code
    for an access token using the code verifier.

    Returns:
        str: The result of the token exchange or an error message.
    """
    # Check CSRF state
    if request.args.get('state') != session.get('state'):
        return "Invalid state. Possible CSRF attack", 400
    logger.info('OAuth callback received and state verified')

    # Check if access denied
    if 'error' in request.args:
        return "Access denied. Possible user denial", 403
    logger.info('Access granted, proceeding with token exchange.')

    # Get authorization code
    auth_code = request.args.get('code')

    # Get code verifier
    code_verifier = session.get('code_verifier')

    # Generate response to get access token
    response = requests.post(
        POST_TOKEN_URL,
        headers={
            "Content-Type": "application/json"
        },
        json={
            "client_id": APPLICATION_ID,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": auth_code,
            "code_verifier": code_verifier
        },
        timeout=10
    )

    # Store token info in database
    store_token_info(response.json())

    return render_template('callback.html')

if __name__ == '__main__':
    logger.info("Initializing database...")
    init_db() # Initialize database
    logger.success("Database initialized successfully.")

    logger.info("Starting Flask application...")
    app.run(debug=True, port=PORT) # Run app
