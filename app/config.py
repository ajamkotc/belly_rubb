SCOPES = [
    "CUSTOMERS_READ",
    "INVENTORY_READ",
    "ORDERS_READ",
    "PAYMENTS_READ"
]
SCOPE_STRING = '+'.join(SCOPES)

SESSION = False

AUTH_URL = "https://connect.squareup.com/oauth2/authorize?"
POST_TOKEN_URL = "https://connect.squareup.com/oauth2/token"
