import os
from dotenv import load_dotenv

load_dotenv()


class URL:
    MAIN = os.getenv("MAIN_URL")
    LOGIN = "login"
    PRODUCT_LIST = "products"
    CART = "view_cart"
    API_PRODUCT_LIST = "api/productsList"

class User:
    MAIL = os.getenv("USER_MAIL")
    PASSWORD = os.getenv("USER_PASSWORD")
