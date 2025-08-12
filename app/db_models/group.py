"""
SQLAlchemy model for the 'groups' table.

Classes:
    Group(Base): Represents a group entity with a unique identifier and name.

    id (str): Primary key, unique identifier for the group.
    name (str): Name of the group.
"""
from sqlalchemy import Column, String
from app.db import Base
print(f"Base defined in group.py: {id(Base)}")

class Group(Base):
    """
    Represents a group entity in the database.

    Attributes:
        id (str): The unique identifier for the group.
        name (str): The name of the group.
    """
    __tablename__ = 'groups'

    id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"
