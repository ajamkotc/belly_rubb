"""
This module defines the SyncState ORM model for tracking synchronization states of resources.

Classes:
    SyncState: Represents the synchronization state for a specific resource,
    including the last sync timestamp and last update timestamp.
"""
#pylint: disable=[E1102]
from sqlalchemy import Column, String

from app.db import Base

class SyncState(Base):
    """
    Represents the synchronization state for a specific resource.

    Attributes:
        resource (str): The name of the resource being tracked. Acts as the primary key.
        last_synced (str): The timestamp of the last successful synchronization
            for the resource.
    """
    __tablename__ = 'sync_states'

    resource = Column(String, primary_key=True)
    last_synced = Column(String, nullable=False)

    def __repr__(self):
        return f"<SyncState(resource={self.resource}, last_synced={self.last_synced})>"
