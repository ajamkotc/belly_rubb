"""
SQLAlchemy ORM model for the 'customers' table.

Classes:
    Customer: Represents a customer.

Attributes:
    id (str): Primary key identifier for the customer.
    locality (str): The locality or area of the customer.
    postal_code (str): Postal code associated with the customer.
    reference_id (str): External reference identifier for the customer.
    note (str): Additional notes or comments about the customer.
    creation_source (str): Source from which the customer record was created.
"""
from sqlalchemy import Column, String
from app.db import Base

class Customer(Base):
    """
    Represents a customer entity in the database.

    Attributes:
        id (str): Primary key identifier for the customer.
        locality (str): The locality or area of the customer.
        postal_code (str): Postal code associated with the customer.
        reference_id (str): External reference identifier for the customer.
        note (str): Additional notes or comments about the customer.
        creation_source (str): Source from which the customer record was created.
    """
    __tablename__ = 'customers'

    id = Column(String, primary_key=True)
    locality = Column(String)
    postal_code = Column(String)
    reference_id = Column(String)
    note = Column(String)
    creation_source = Column(String)

    def __repr__(self):
        return f"<Customer(id={self.id}, \
            locality={self.locality}, postal_code={self.postal_code}, \
            reference_id={self.reference_id}, \
            note={self.note}, creation_source={self.creation_source})>"
