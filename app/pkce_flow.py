import os
import secrets
import hashlib
import base64
import requests
from flask import Flask, render_template, session, redirect, request
from dotenv import load_dotenv

from app.config import SCOPE_STRING, AUTH_URL, SESSION

load_dotenv()
APPLICATION_ID = os.getenv("SQUARE_SANDBOX_APPLICATION_ID")

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

    # Code verifier
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier

    # Generate authorization url
    auth_url = (
        AUTH_URL +
        f"?client_id={APPLICATION_ID}"
        f"&scope={SCOPE_STRING}"
        f"&session={SESSION}"
        f"&state={state}"
        f"&code_challenge={generate_code_challenge(code_verifier)}"
    )

    return redirect(auth_url)

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

    # Check if access denied
    if 'error' in request.args:
        return "Access denied. Possible user denial", 403

    # Exchange authorization code for access token
    code = request.args.get('code')
    code_verifier = session.get('code_verifier')

    token_response = exchange_code_for_token(code, code_verifier)

    if token_response.get("error"):
        return f"Error: {token_response['error_description']}", 400

    return "Authorization successful", 200
