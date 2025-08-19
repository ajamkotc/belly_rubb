import os
from dotenv import load_dotenv
from datetime import datetime
from square import Square
from sqlalchemy import select, func

from app.db import Session
from app.db_models.order import Order

from belly_rubb.etl.api_manager import APIManager
from belly_rubb.etl.token_provider import TokenProvider

load_dotenv()
LOCATION_ID = os.getenv(key="BELLY_RUBB_LOCATION_ID")

class OrdersAPI:
    def __init__(self, merchant_id: str):
        # Initialize the token provider
        provider = TokenProvider()
        access_token = provider.get_access_token(merchant_id=merchant_id)

        # Square client to make API requests
        self.client = Square(token=access_token)

        # API Manager for handling synchronization
        self.api_manager = APIManager()

    def _get_latest_order(self, session) -> datetime:
        """
        Retrieves the latest order's updated_at timestamp from the database.

        Params:
            session: Database session to use for the operation.
        
        Returns:
            result (datetime): The latest order's updated_at timestamp.
        """
        stmt = select(func.max(Order.updated_at))
        result = session.execute(stmt).scalar_one()

        return result

    def get_order_ids(self, location_ids: list, return_entries: bool = False, page_limit: int = 500):
        

        response = self.client.orders.search(
            return_entries=return_entries,
            limit=page_limit,
            location_ids=location_ids
        )

    def _paginated_orders(self, page_limit: int = 50):
        pass

    def sync_orders(self):
        with Session() as session_db:
            print(self._get_latest_order(session_db))

if __name__ == "__main__":
    orders_sync = OrdersAPI(merchant_id="MLW4W4RYAASNM")
    orders_sync.sync_orders()
    # Example usage to get order IDs
    # print(orders_sync.get_order_ids(location_ids=[LOCATION_ID], return_entries=True, page_limit=100))
