from square import Square

from app.db import Session
from belly_rubb.etl.token_provider import TokenProvider

class OrdersAPI:
    def __init__(self, merchant_id: str):
        provider = TokenProvider()
        token = provider.get_access_token(merchant_id=merchant_id)

        self.client = Square(token=token)

    def _get_order_ids(self):
        pass