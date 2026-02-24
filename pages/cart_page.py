from selenium.common import TimeoutException
from allure_commons._allure import step

from locators import cart_locators as loc
from pages.main_page import MainPage
from utils.models import Product


class CartPage(MainPage):
    # Actions
    @step
    def delete_all_products(self):
        try:
            product_element_list = self.wait_all_elements(loc.product_list, timeout=10)
        except TimeoutException:
            product_element_list = []

        for product_element in product_element_list:
            self.click_on(loc.product_delete_button, parent=product_element)

    # Read
    @step
    def get_product_list(self):
        product_element_list = self.wait_all_elements(loc.product_list)

        product_list = []
        for product_element in product_element_list:
            product = Product(
                name=self.get_text(loc.product_name, parent=product_element),
                price=self.get_text(loc.product_price, parent=product_element),
                cart_quantity=int(self.get_text(loc.product_quantity, parent=product_element)),
            )
            product_list.append(product)

        return product_list
