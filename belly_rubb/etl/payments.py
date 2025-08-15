from loguru import logger
from square import Square
from sqlalchemy.dialects.sqlite import insert

from belly_rubb.etl.token_provider import TokenProvider
from belly_rubb.etl.api_manager import APIManager

class PaymentAPI:
    def __init__(self, merchant_id: str):
        # Initialize token provider to get access token
        token_provider = TokenProvider()
        token = token_provider.get_access_token(merchant_id=merchant_id)

        # Initialize Square client to make API requests
        self.square_client = Square(token=token)

        # Initialize API Manager for handling synchronization
        self.api_manager = APIManager()

    def pull_payments(self, page_limit: int = 50):
        """
        Retrieves payment records from the API in a paginated manner.

        Args:
            page_limit (int): The maximum number of payment records to retrieve per API request.

        Yields:
            dict: Individual payment records obtained from the API.

        Notes:
            - The method uses a cursor-based pagination to fetch all available payment records.
            - Records are sorted by 'created_at' in descending order.
            - If the API request fails or no payments are found, the process stops.
        """
        cursor = None

        while True:
            api_response = self.square_client.payments.list(
                sort_field='UPDATED_AT',
                limit=page_limit,
                cursor=cursor
            )

            # Check if the API response was successful
            if not api_response.is_success():
                logger.info("No payments found or API request failed.")
                return

            # Extract the body from the API response
            data = api_response.body

            # Generate payment records
            yield from self.api_manager.iter_records(
                records=data.get('payments', []),
                resource='payments'
            )

            cursor = data.get('cursor')
            if not cursor:
                break

    def store_payment_info(self, payment_info: dict) -> None:
        pass