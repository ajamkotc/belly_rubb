OAuth Setup
===========

## Overview
1. **Authorization**: Application uses an authorization URL to send the seller to the Square authorization page.
2. **Callback**: Square uses the *redirect URL* to send the seller back to the application and appends an authorization code query parameter.
3. **Token request**: Application sends authorization code and other fields. Square returns an access token and refresh token to access the data.

### Requirements and Limitations
- OAuth API requires HTTPS for the redirect URL. HTTP can be used for testing. 
- Authorization codes expire after 5 minutes and can only be used once.
- Access tokens expire after 30 days. New tokens can be generated using the refresh token.
- Refresh tokens obtained using the PKCE flow are single-use and expire after 90 days.

### [PKCE (Proof Key for Code Exchange) Flow](https://developer.squareup.com/docs/oauth-api/overview#pkce-flow)
Designed for public clients that shouldn't store secret information (vs [*code flow*](https://developer.squareup.com/docs/oauth-api/overview#code-flow)).
1. Client application builds an authorization URL.
2. Client application creates a `code_verifier` and uses the Base64-URL-encoding of its SHA256 hash to create the `code_challenge`.
3. Authorization request calls the `Authorize` endpoint and includes the `code_challenge`.
4. `Authorize` endpoint returns an authorization code by making a `GET` request to the *redirect URL*. The server retains the `code_challenge`.
5. The client calls the `ObtainToken` endpoint and provides parameters including the authorization code and `code_verifier`. The server verifies that the `code_verifier` is the same value as that which was encrypted to create the `code_challenge`.
6. `ObtainToken` endpoint returns the access token.

## Key Components
- `auth()` - Generates the authorization URL with PKCE and redirects the user to Square.
- `callback()` - Validates the state, retrieves the token, and stores it in a database.
- `generate_code_challenge()` - Generates the `code_challenge` from a randomly generated `code_verifier`.
- `store_token_info()` - Stores the token in the database.

## Security notes
- This app uses a randomly generated `state` to prevent CSRF attacks.
- OAuth secrets and tokens are never logged.
- Environment variables are loaded from a `.env` file (not committed).
