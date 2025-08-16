from square import Square
<<<<<<< HEAD
from belly_rubb.etl.api_manager import APIManager
from belly_rubb.etl.token_provider import TokenProvider


class OrdersAPI:
    def __init__(self, merchant_id: str):
        # Initialize the token provider
        provider = TokenProvider()
        access_token = provider.get_access_token(merchant_id=merchant_id)

        # Square client to make API requests
        self.client = Square(token=access_token)

        # API Manager for handling synchronization
        self.api_manager = APIManager()

    def _paginated_orders(self, page_limit: int = 50):
=======

from app.db import Session
from belly_rubb.etl.token_provider import TokenProvider

class OrdersAPI:
    def __init__(self, merchant_id: str):
        provider = TokenProvider()
        token = provider.get_access_token(merchant_id=merchant_id)

        self.client = Square(token=token)

    def _get_order_ids(self):
>>>>>>> 8fba5b64c3b48975e03f8a792eb695cf9bc01310
        pass