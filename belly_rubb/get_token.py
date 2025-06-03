"""
Flask application for authenticating with the Square API using OAuth2.

This app guides the user through the OAuth authorization flow with Square:
1. Displays a landing page with a button to initiate the OAuth process.
2. Redirects the user to Square's authorization server with the required scopes.
3. Handles the callback from Square after the user authorizes the app.
4. Verifies the returned state parameter to prevent CSRF attacks.
5. Exchanges the authorization code for an access token via Square's token endpoint.
6. Stores the received token information securely in a local JSON file.

Environment variables required:
- SQUARE_APPLICATION_ID: Your Square application client ID
- SQUARE_APPLICATION_SECRET: Your Square application client secret

Dependencies:
- Flask
- requests
- python-dotenv
- secrets
- os
- json
"""
import os
import secrets
import json
from flask import Flask, request, redirect, session
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.secret_key = secrets.token_urlsafe(32)

APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID")
APPLICATION_SECRET = os.getenv("SQUARE_APPLICATION_SECRET")

@app.route('/')
def home():
    """
    Render the home page with a styled button that links to the Square OAuth authorization route.
    """
    # Generate hyperlink to auth
    return """
        <html>
        <head>
            <title>Connect to Square</title>
            <style>
            body {
                font-family: sans-serif;
                text-align: center;
                padding-top: 100px;
            }
            .button {
                background-color: #0072CE;
                border: none;
                color: white;
                padding: 15px 30px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 6px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #005bb5;
            }
            </style>
        </head>
        <body>
            <h1>Authorize Arsen's App with Square</h1>
            <a href="/auth" class="button">Connect Square</a>
        </body>
        </html>
    """

@app.route('/auth')
def auth():
    """
    Generate a unique state token, store it in the session, 
    and redirect the user to Square's OAuth authorization URL.
    """
    # Generate state and save in session
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    # Generate authorization url
    auth_url = (
        "https://connect.squareup.com/oauth2/authorize"
        f"?client_id={APPLICATION_ID}"
        "&scope=CUSTOMERS_READ+INVENTORY_READ+ORDERS_READ+PAYMENTS_READ"
        "&session=False"
        f"&state={state}"
    )

    return redirect(auth_url)

@app.route('/callback')
def callback():
    """
    Handle the OAuth callback from Square.

    Validates the returned state parameter against the session-stored state to prevent CSRF.
    Exchanges the authorization code for an access token by posting to Square's token endpoint.
    Saves the received token data to a local JSON file and renders a confirmation page.
    """
    # Check if returned state is the same as generated state
    returned_state = request.args.get('state')
    expected_state = session['oauth_state']

    if returned_state != expected_state:
        return "State mismatch! Possible CSRF attack.", 400

    # Get code returned by Square
    code = request.args.get('code')

    # Post code to Square to get access token
    response = requests.post(
        "https://connect.squareup.com/oauth2/token",
        headers={
            "Square-Version": "2025-05-21", 
            "Authorization": "Bearer ACCESS_TOKEN",
            "Content-Type": "application/json"},
        json={
            "client_id": APPLICATION_ID,
            "client_secret": APPLICATION_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        },
        timeout=10
    )

    # Get response from Square
    token_info = response.json()

    # Save response in json format
    with open("secrets.json", "w", encoding='utf-8') as f:
        json.dump(token_info, f, indent=2)

    return """
        <html>
        <head><title>Square OAuth</title></head>
        <body>
            <h2>✅ Authorization Complete</h2>
            <p>You can now close this window and return to the app.</p>
        </body>
        </html>
    """

if __name__ == '__main__':
    app.run(port=8000)
