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
    * `created_at` (timestamp) - Timestamp of when customer record was created.
    * `updated_at` (timestamp) - Timestamp of latest update to ercord.
    * `given_name` (varchar) - First name of customer.
    * `family_name` (varchar) - Last name of customer, defaults to `""`.
    * `locality` (varchar) - The locality or area of a customer.
    * `postal_code` (integer) - Postal code associated with the customer.
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

### sync_states
* **Purpose**: Stores the sync states for table resources.
* **Columns**:

    * `resource` (varchar) - primary key - Name of resource.
    * `last_synced` (timestamp) - Date it was last synced.
    * `updated` (timestamp) - Date record was updated.

### payments
* **Purpose**: Stores payment information for sales.
* **Columns**:

    * `id` (varchar) - primary key - Unique identifier for payment.
    * `created_at` (timestamp) - Timestamp when payment was created.
    * `updated_at` (timestamp) - Timestamp when payment was last updated.
    * `status` (str) - Current status of the payment.
    * `amount` (float) - Amount of the payment.
    * `total_money` (float) - Total money involved in the payment.
    * `approved_money` (float) - Amount of money approved for the payment.
    * `currency` (str) - Currency code for the payment.
    * `card_brand` (str) - Brand of the card used for the payment.
    * `location_id` (str) - Identifier for the location where payment was made.
    * `order_id` (str) - foreign key - References the associated order.
    * `square_product` (str) - Product identifier from Square.
