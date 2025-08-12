"""
SQLAlchemy model for representing the membership relationship between a customer and a group.

Classes:
    GroupMembership(Base): ORM model for the 'group_memberships' table.

    customer_id (str): Foreign key referencing the customer's ID in the 'customers' table.
    group_id (str): Foreign key referencing the group's ID in the 'groups' table.

Methods:
    __repr__(): Returns a string representation of the GroupMembership instance.
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from app.db import Base

class GroupMembership(Base):
    """
    Represents a membership relationship between a customer and a group.

    Attributes:
        id (int): Primary key, unique identifier for the group membership.
        customer_id (str): Foreign key referencing the customer's ID.
        group_id (str): Foreign key referencing the group's ID.
    """
    __tablename__ = 'group_memberships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, ForeignKey('customers.id'))
    group_id = Column(String, ForeignKey('groups.id'))

    def __repr__(self):
        return f"<GroupMembership(id={self.id}, customer_id={self.customer_id}, \
            group_id={self.group_id})>"
