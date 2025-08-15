"""
APIManager provides methods for managing synchronization states and filtering records
for ETL processes.

This class enables:
- Checking if records are more recent than the last synchronization for a resource.
- Iterating over records and yielding those updated since the last sync.

Classes:
    APIManager:
                Determines if a record's creation date is more recent than the last sync date
                for the specified resource.
"""
from datetime import datetime, timezone
from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from dateutil import parser

from app.db import Session
from app.db_models import SyncState
from app.pkce_flow import iso_to_utc

class APIManager:
    """
    APIManager provides methods for managing synchronization states and filtering records.

    This class is designed to facilitate ETL processes by:
    - Determining if records are more recent than the last synchronization.
    - Upserting synchronization state information in the database.
    - Iterating over records and yielding those that have been updated since the last sync.

    Methods:
        _is_recent(resource: str, record_date: datetime, session) -> bool:
            Checks if a record's creation date is more recent than the last sync date
                for a given resource.
        _upsert_sync_state(resource: str, session) -> None:
            Inserts or updates the synchronization state for a resource in the database.
        iter_records(records: list, resource: str):
            Yields records that have been updated since the last synchronization and
                updates the sync state after processing.
    """
    def _is_recent(self, resource: str, record_date: datetime, session) -> bool:
        """
        Determines if a customer's creation date is more recent than the last sync date.

        Args:
            resource (str): The resource being checked.
            record_date (datetime): The creation timestamp of the record.
            session: Database session to use for the operation.

        Returns:
            bool: True if the record was created after the last sync date or no sync state exists,
                False otherwise.
        """
        # Retrieve sync state
        stmt = (
            select(SyncState)
            .where(SyncState.resource == resource)
        )
        # Execute query to get sync state
        sync_state = session.execute(stmt).scalars().first()

        # If it doesn't exist assume record is recent
        if not sync_state:
            return True

        return record_date > parser.isoparse(sync_state.last_synced)

    def _upsert_sync_state(self, resource: str, session) -> None:
        """
        Upserts the synchronization state for the current resource in the database.

        This method inserts a new sync state record for the resource if it does not exist,
        or updates the `last_synced` timestamp if it does. The operation is performed
        using an upsert (insert or update on conflict) statement.

        Logs the upsert operation before and after execution.

        Params:
            resource (str): Resource to update.
            session: Database session to use for the operation.

        Returns:
            None
        """
        stmt = insert(SyncState).values(
            resource=resource,
            last_synced=iso_to_utc(datetime.now(timezone.utc))
        )

        update_dict = {
            "last_synced": iso_to_utc(datetime.now(timezone.utc))
        }
        stmt = stmt.on_conflict_do_update(index_elements=['resource'], set_=update_dict)

        logger.debug(f"Upserting sync state for resource: {resource}")

        session.execute(stmt)

    def iter_records(self, records: list, resource: str):
        """
        Iterates over a list of records and yields recently updated records.

        Compares 'updated_at' date of record with the last sync date. Updates the sync date
        after iterating through records.

        Args:
            records (list): A list containing record data.
                Each record should have an 'updated_at' field.
            resource (str): Name of the resource being synchronized.

        Yields:
            dict: Records that have been updated since the last synchronization.
        """
        with Session() as session:
            with session.begin():
                try:
                    for record in records:
                        # Get date record was updated
                        record_updated = parser.isoparse(record.updated_at)

                        # Check if record updated since last sync
                        if self._is_recent(resource, record_updated, session):
                            yield record
                finally:
                    # Update sync state
                    self._upsert_sync_state(resource, session)
                    logger.success(f"Sync state updated for resource: {resource}")
