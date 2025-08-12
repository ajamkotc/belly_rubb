CREATE TABLE group_membership (
    id INT PRIMARY KEY,
    customer_id VARCHAR FOREIGN KEY REFERENCES customers(id),
    group_id VARCHAR FOREIGN KEY REFERENCES groups(id)
);