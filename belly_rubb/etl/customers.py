"""
Module: customers.py

This module provides the CustomerAPI class for synchronizing customer data
between an external API (Square) and a local database.

Classes:
    CustomerAPI:
        - Provides methods to interact with customer data from the Square API.
        - Handles authentication, API requests, pagination, and database synchronization.
        - Methods:
            - __init__(merchant_id: str): Initializes the API client and synchronization manager.
            - _paginated_customers(page_limit: int): Retrieves customer records from the API.
            - _store_customer_info(customer_info: dict): Inserts or updates customer data
                                                            in the database.
            - sync_customers(page_limit: int = 50): Synchronizes customer data between the API
                                                            and the database.

Dependencies:
    - dateutil.parser: For parsing ISO date strings.
    - square.Square: Square API client.
    - loguru.logger: Logging utility.
    - sqlalchemy.dialects.sqlite.insert: For upsert operations in SQLite.
    - app.db.Session: SQLAlchemy session for database operations.
    - app.db_models.Customer: SQLAlchemy model for customer records.
    - belly_rubb.etl.token_provider.TokenProvider: Provides API access tokens.
    - belly_rubb.etl.api_manager.APIManager: Manages API synchronization and record iteration.

Usage:
    Instantiate CustomerAPI with a merchant ID and call sync_customers() to sync customer data.
"""
import time
from dateutil import parser
from square import Square
from square.core.api_error import ApiError
from loguru import logger

from sqlalchemy.dialects.sqlite import insert

from app.db import Session
from app.db_models import Customer
from belly_rubb.config import MAX_RETRIES, INITIAL_DELAY, DECAY_BASE
from belly_rubb.etl.token_provider import TokenProvider
from belly_rubb.etl.api_manager import APIManager

class CustomerAPI:
    """
    CustomerAPI provides methods to interact with customer data from an external API.

    Downloaded records are synchronized with a local database.

    Attributes:
        client (Square): Instance of the Square API client for making customer-related API requests.
        api_manager (APIManager): Manages API synchronization state and record iteration.

    Methods:
        __init__(merchant_id: str):
            Initializes the CustomerAPI with the merchant ID, sets up authentication,
                and prepares API clients.
        _paginated_customers(page_limit: int):
            Generates pages of customer records from the API yielding a list of Customers.
        _store_customer_info(customer_info: dict) -> None:
            Inserts or updates customer information in the database.
                Handles conflicts by updating existing records.
        sync_customers(page_limit: int = 50):
            Synchronizes customer data between the API and database, logging progress and results.
    """

    def __init__(self, merchant_id: str):
        # Initialize token provider to get access token
        provider = TokenProvider()
        access_token = provider.get_access_token(merchant_id=merchant_id)

        # Square client to make API requests
        self.client = Square(token=access_token)

        # API Manager for handling synchronization state
        self.api_manager = APIManager()

    def _paginated_customers(self, page_limit: int = 50):
        """
        Generates pages of customer records from the API.

        Uses exponential delay to delay API requests in case of rate limit error.

        Params:
            page_limit (int): Limit of records per page

        Yields:
            list: List of Customer objects from API.
        """
        # Set initial values for exponential delay
        delay = INITIAL_DELAY
        base = DECAY_BASE
        retries = 1

        try:
            api_response = self.client.customers.list(
                limit=page_limit,
                sort_field='CREATED_AT',
                sort_order='DESC'
            )
        except ApiError as e:
            if e.status_code == 429 and retries <= MAX_RETRIES:
                logger.warning(f"Rate limit exceeded. Retrying after delay. Attempt {retries}")

                # Retry logic for rate limit errors
                delay = base ** retries  # Exponential backoff
                time.sleep(delay)

                retries += 1
            else:
                logger.error(f"Error fetching paginated customers: {e}")
                return

        for page in api_response.iter_pages():
            yield page

    def _store_customer_info(self, customer_info: dict) -> None:
        """
        Inserts or updates customer information in the database.

        If a customer with the given 'id' already exists, their record is updated
        with the new information. Otherwise, a new customer record is created.

        Args:
            customer_info (dict): A dictionary containing customer details. Expected keys:
                - 'id' (str): Unique identifier for the customer.
                - 'address' (dict): Dictionary with keys 'locality' and 'postal_code'.
                - 'reference_id' (str): Reference identifier for the customer.
                - 'note' (str): Additional notes about the customer.
                - 'creation_source' (str,): Source of customer creation.

        Returns:
            None
        """
        address = customer_info.get('address', {}) # Have default in case empty

        # Attempt to insert Customer into table
        stmt = insert(Customer).values(
            id=customer_info.get('id'),
            created_at=parser.isoparse(customer_info.get('created_at')),
            updated_at=parser.isoparse(customer_info.get('updated_at')),
            given_name=customer_info.get('given_name'),
            family_name=customer_info.get('family_name'),
            locality=address.get('locality'),
            postal_code=address.get('postal_code'),
            reference_id=customer_info.get('reference_id'),
            note=customer_info.get('note'),
            creation_source=customer_info.get('creation_source')
        )

        # Create dictionary mapping updated values to current entry in db
        update_dict = {}
        for col in Customer.__table__.columns:
            if col.name not in ['id', 'created_at']:
                update_dict[col.name] = stmt.excluded[col.name]

        with Session() as session_db:
            # Execute statement and update if conflict occurs
            session_db.execute(stmt.on_conflict_do_update(index_elements=['id'], set_=update_dict))
            session_db.commit()

    def sync_customers(self, page_limit: int=50) -> None:
        """
        Synchronizes customer data between the API and the database.

        Args:
            page_limit (int): The maximum number of records to retrieve per API request.

        Returns:    
            None
        """
        logger.info("Starting customer synchronization process.")
        count_of_records = 0

        # Loop through customer records
        for page in self._paginated_customers(page_limit=page_limit):
            # Loop through records in page
            for record in self.api_manager.iter_records(records=page, resource='customers'):
                # Store customer data
                self._store_customer_info(record.dict())

                count_of_records += 1

        logger.success(f"Customer synchronization process completed successfully. "
                       f"Stored {count_of_records} records.")

if __name__ == "__main__":
    customer_sync = CustomerAPI(merchant_id="MLW4W4RYAASNM")
    customer_sync.sync_customers()
