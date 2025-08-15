CREATE TABLE customers (
    id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    given_name VARCHAR,
    family_name VARCHAR DEFAULT "",
    locality VARCHAR,
    postal_code INTEGER,
    reference_id VARCHAR,
    note VARCHAR,
    creation_source VARCHAR
);