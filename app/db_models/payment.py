"""
SQLAlchemy ORM model for the 'payments' table.

Classes:
    Payment: Represents a payment transaction.

Attributes:
    id (str): Unique identifier for the payment.
    created_at (str): Timestamp when the payment was created.
    updated_at (str): Timestamp when the payment was last updated.
    status (str): Current status of the payment.
    amount (float): Amount of the payment.
    total_money (float): Total money involved in the payment.
    approved_money (float): Amount of money approved for the payment.
    currency (str): Currency code for the payment.
    card_brand (str): Brand of the card used for the payment.
    location_id (str): Identifier for the location where the payment was made.
    order_id (str): Foreign key referencing the associated order.
    square_product (str): Product identifier from Square.
"""
from sqlalchemy import Column, String, Float, ForeignKey
from app.db import Base

class Payment(Base):
    """
    Represents a payment transaction in the system.
    Attributes:
        id (str): Unique identifier for the payment.
        created_at (str): Timestamp when the payment was created.
        updated_at (str): Timestamp when the payment was last updated.
        status (str): Current status of the payment.
        amount (float): Amount of the payment.
        total_money (float): Total money involved in the payment.
        approved_money (float): Amount of money approved for the payment.
        currency (str): Currency code for the payment.
        card_brand (str): Brand of the card used for the payment.
        location_id (str): Identifier for the location where the payment was made.
        order_id (str): Foreign key referencing the associated order.
        square_product (str): Product identifier from Square.
    """
    __tablename__ = "payments"

    id = Column(String, primary_key=True)
    created_at = Column(String)
    updated_at = Column(String)
    status = Column(String)
    amount = Column(Float)
    total_money = Column(Float)
    approved_money = Column(Float)
    currency = Column(String)
    status = Column(String)
    card_brand = Column(String)
    location_id = Column(String)
    order_id = Column(String, ForeignKey("orders.id"))
    square_product = Column(String)

    def __repr__(self):
        return f"<Payment(id={self.id}, status={self.status}, amount={self.amount})>"
