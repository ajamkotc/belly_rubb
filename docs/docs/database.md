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

### customers
* **Purpose**: Stores customer information.
* **Columns**:

    * `id` (varchar) - primary key - Customer's unique identifier.
    * `locality` (varchar) - The locality or area of a customer.
    * `postal_code` (varchar) - Postal code associated with the customer.
    * `reference_id` (varchar) - External reference identifier for the customer.
    * `note` (varchar) - Additional notes or comments about the customer.
    * `creation_source` (varchar) - Source from which the customer record was created.

### groups
* **Purpose**: Stores customer group information.
* **Columns**:

    * `id` (varchar) - primary key - Unique identifier for group.
    * `name` (varchar) - Name of group.

### group_memberships
* **Purpose**: Stores group membership information.
* **Columns**:

    * `id` (varchar) - primary key - Row number.
    * `customer_id` (varchar) - foreign key - Links to customer `id`.
    * `group_id` (varchar) - foreign key - Links to group `id`.