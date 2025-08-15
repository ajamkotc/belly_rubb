CREATE TABLE payments (
    id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    status VARCHAR,
    amount FLOAT,
    total_money FLOAT,
    approved_money FLOAT,
    currency VARCHAR,
    card_brand VARCHAR,
    location_id VARCHAR,
    order_id VARCHAR REFERENCES orders(id),
    square_product VARCHAR
)