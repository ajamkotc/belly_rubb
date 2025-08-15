CREATE TABLE tokens (
    merchant_id VARCHAR PRIMARY KEY,
    access_token VARCHAR,
    token_type VARCHAR,
    expires_at VARCHAR,
    refresh_token VARCHAR,
    short_lived BOOLEAN DEFAULT FALSE,
    refresh_token_expires_at VARCHAR,
    created_at VARCHAR DEFAULT CURRENT_TIMESTAMP
);
