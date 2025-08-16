from square import Square
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
        pass