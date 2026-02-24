import requests

from settings import URL
from utils.models import Product


class Api:
    @staticmethod
    def get_product_list():
        request = requests.get(URL.MAIN + URL.API_PRODUCT_LIST)
        api_product_list = request.json().get("products")

        product_list = []
        for api_product in api_product_list:
            product = Product(
                name=api_product.get("name"),
                price=api_product.get("price"),
                id=api_product.get("id"),
                brand=api_product.get("brand"),
                category=api_product.get("category"),
            )
            product_list.append(product)

        return product_list
