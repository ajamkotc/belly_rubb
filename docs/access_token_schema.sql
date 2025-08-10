CREATE TABLE tokens (
    merchant_id VARCHAR PRIMARY KEY,
    access_token VARCHAR,
    token_type VARCHAR,
    expires_at TIMESTAMP,
    refresh_token VARCHAR,
    short_lived BOOLEAN DEFAULT FALSE,
    refresh_token_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
