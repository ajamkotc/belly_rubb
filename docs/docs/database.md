Database Schema
===============

## Overview

## Tables

### access_tokens
* **Purpose**: Stores access tokens provided by sellers.
* **Columns**:

    * `merchant_id` (varchar) - primary key - Merchant's unique identifier.
    * `access_token` (varchar) - Token to use when making Square API calls.
    * `token_type` (varchar) - Level of data access granted.
    * `expires_at` (timestamp) - Expiration date of access token.
    * `refresh_token` (varchar) - Token to refresh access token without repeating full OAuth process.
    * `short_lived` (boolean) - Deprecated, False by default.
    * `refresh_token_expires_at` (timestamp) - Expiration date of the refresh token.
    * `created_at` (timestamp) - Creation date of access token.