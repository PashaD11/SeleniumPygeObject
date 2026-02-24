import random

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.product_list_page import ProductListPage
from settings import URL, User
from utils.api import Api


class TestProduct:
    def test_add_product_to_cart(self, driver, empty_cart_after_test):
        email = User.MAIL
        password = User.PASSWORD

        api_product_list = Api.get_product_list()

        product = random.choice(api_product_list)

        login_page = LoginPage(driver)
        product_list_page = ProductListPage(driver)
        cart_page = CartPage(driver)

        login_page.login_and_go_to(email, password, URL.CART)
        cart_page.delete_all_products()

        product_list_page.go_to(URL.MAIN + URL.PRODUCT_LIST)

        product_list_page.add_product_to_cart_by_name(product.name)
        assert product_list_page.check_cart_modal_present(), "Cart Modal is not present"

        product_list_page.click_view_cart_link()

        cart_product_list = cart_page.get_product_list()
        assert len(cart_product_list) == 1, f"Expects only one cart item. Cart product list - {cart_product_list}"

        actual_product = cart_product_list[0]
        assert actual_product.name == product.name, \
            f"Cart product name actual - {actual_product.name}, expected - {product.name}"
        assert actual_product.price == product.price, \
            f"Cart product price actual - {actual_product.price}, expected - {product.price}"
        assert actual_product.cart_quantity == 1, \
            f"Cart product quantity actual - {actual_product.cart_quantity}, expected - 1"
