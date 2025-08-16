"""
Module: payments.py

This module provides the PaymentAPI class for synchronizing payment data
between an external API (Square) and a local database.

Classes:
    PaymentAPI:
        - Provides methods to interact with payment data from the Square API.
        - Handles authentication, API requests, pagination, and database synchronization.
        - Methods:
            - __init__(merchant_id: str): Initializes the API client and synchronization manager.
            - _paginated_payments(page_limit: int): Retrieves payment records from the API.
            - _store_payment_info(payment_info: dict): Inserts or updates payment data
                                                            in the database.
            - sync_payments(page_limit: int = 50): Synchronizes payment data between the API
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
    Instantiate PaymentAPI with a merchant ID and call sync_payments() to sync payment data.
"""
import time
<<<<<<< HEAD
from datetime import datetime, timezone
=======
from datetime import datetime
>>>>>>> 8fba5b64c3b48975e03f8a792eb695cf9bc01310
from dateutil import parser
from loguru import logger
from square import Square
from square.core.api_error import ApiError

from sqlalchemy import select, func
from sqlalchemy.dialects.sqlite import insert

from app.pkce_flow import iso_to_utc
from app.db import Session
from app.db_models import Payment
from belly_rubb.config import MAX_RETRIES, INITIAL_DELAY, DECAY_BASE
from belly_rubb.etl.token_provider import TokenProvider
from belly_rubb.etl.api_manager import APIManager

class PaymentAPI:
    """
    PaymentAPI provides methods to interact with payment data from an external API.

    Downloaded records are synchronized with a local database.

    Attributes:
        client (Square): Instance of the Square API client for making payment-related API requests.
        api_manager (APIManager): Manages API synchronization state and record iteration.

    Methods:
        __init__(merchant_id: str):
            Initializes the PaymentAPI with the merchant ID, sets up authentication,
                and prepares API clients.
        _paginated_payments(page_limit: int):
            Generates pages of payment records from the API yielding a list of Payments.
        _store_payment_info(payment_info: dict) -> None:
            Inserts or updates payment information in the database.
                Handles conflicts by updating existing records.
        sync_payments(page_limit: int = 50):
            Synchronizes payment data between the API and database, logging progress and results.
    """
    def __init__(self, merchant_id: str):
        # Initialize token provider to get access token
        token_provider = TokenProvider()
        token = token_provider.get_access_token(merchant_id=merchant_id)

        # Initialize Square client to make API requests
        self.client = Square(token=token)

        # Initialize API Manager for handling synchronization
        self.api_manager = APIManager()

    def _paginated_payments(self, page_limit: int = 50):
        """
        Generates pages of payment records from the API.

        Uses exponential delay to delay API requests in case of rate limit error.

        Params:
            page_limit (int): Limit of records per page

        Yields:
            list: List of Payment objects from API.
        """
        # Set initial values for exponential delay
        delay = INITIAL_DELAY
        retries = 1
        base = DECAY_BASE

        try:
            api_response = self.client.payments.list(
                limit=page_limit,
                sort_field='UPDATED_AT',
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
                logger.error(f"Error fetching paginated payments: {e}")
                return

        for page in api_response.iter_pages():
            yield page

    def _store_payment_info(self, payment_info: dict, session) -> None:
        """
        Inserts or updates payment information in the database.

        If a payment with the given 'id' already exists, their record is updated
        with the new information. Otherwise, a new payment record is created.

        Args:
            payment_info (dict): A dictionary containing customer details. Expected keys:
                - 'id' (str): Unique identifier for the payment.
                - 'created_at' (str): Timestamp when the payment was created.
                - 'updated_at' (str): Timestamp when the payment was last updated.
                - 'status' (str): Current status of the payment.
                - 'amount' (float): Amount of the payment.
                - 'total_money' (float): Total money involved in the payment.
                - 'approved_money' (float): Amount of money approved for the payment.
                - 'currency' (str): Currency code for the payment.
                - 'card_brand' (str): Brand of the card used for the payment.
                - 'location_id' (str): Identifier for the location where the payment was made.
                - 'order_id' (str): Foreign key referencing the associated order.
                - 'square_product' (str): Product identifier from Square.
            session: Database session to use for the operation.

        Returns:
            None
        """
        amount_money = payment_info.get('amount_money', {})
        total_money = payment_info.get('total_money', {})
        card_details = payment_info.get('card_details', {})
        card = card_details.get('card', {})
        approved_money = payment_info.get('approved_money', {})

        # Attempt to insert Payment into table
        stmt = insert(Payment).values(
            id=payment_info.get('id'),
            created_at=parser.isoparse(payment_info.get('created_at')),
            updated_at=parser.isoparse(payment_info.get('updated_at')),
            status=card_details.get('status'),
            amount=amount_money.get('amount'),
            total_money=total_money.get('total_money'),
            approved_money=approved_money.get('approved_money'),
            currency=amount_money.get('currency'),
            card_brand=card.get('card_brand'),
            location_id=payment_info.get('location_id'),
            order_id=payment_info.get('order_id'),
            square_product=payment_info.get('square_product')
        )

        # Create dictionary mapping updated values to current entry in db
        update_dict = {}
        for col in Payment.__table__.columns:
            if col.name not in ['id', 'created_at']:
                update_dict[col.name] = stmt.excluded[col.name]

        # Execute statement and update if conflict occurs
        session.execute(stmt.on_conflict_do_update(index_elements=['id'], set_=update_dict))


    def get_most_recent_payment(self, session):
        stmt = select(func.max(Payment.updated_at))

        result = session.execute(stmt).scalar_one()
        return result

    def sync_payments(self, page_limit: int = 50):
        """
        Synchronizes payment data between the API and the database.

        Args:
            page_limit (int): The maximum number of records to retrieve per API request.

        Returns:    
            None
        """
        logger.info("Starting payment synchronization process...")
        count_of_records = 0
        last_synced = iso_to_utc(datetime.now(timezone.utc))

        with Session() as session_db:
            # Loop through payment records.
            for page in self._paginated_payments(page_limit=page_limit):
                # Loop through records on page
                for payment in self.api_manager.iter_records(
                    records=page, resource='payments', sorted_by_updated=True):
                    # Store payment data
                    self._store_payment_info(payment.dict(), session=session_db)

                    count_of_records += 1

            logger.success(f"Payment synchronization process completed. " \
                            f"Total records processed: {count_of_records}")
            last_synced = iso_to_utc(datetime.now(timezone.utc))

            # Upsert sync state
            self.api_manager.upsert_sync_state(
                resource='payments',
                last_synced=last_synced,
                session=session_db
            )
            session_db.commit()

if __name__ == "__main__":
    payment_sync = PaymentAPI(merchant_id="MLW4W4RYAASNM")
    payment_sync.sync_payments()
