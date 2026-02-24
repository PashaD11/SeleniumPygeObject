import pytest
from allure_commons._allure import step

from locators import product_list_locators as loc
from pages.main_page import MainPage


class ProductListPage(MainPage):
    # Actions
    @step
    def add_product_to_cart_by_name(self, name):
        product_list = self.wait_all_elements(loc.product_list)
        for product in product_list:
            product_name = self.get_text(loc.product_name, parent=product)
            if product_name == name:
                self.click_on(loc.product_add_to_cart_button, parent=product)
                break
        else:
            pytest.fail(f"Product {name} not found")

    @step
    def click_view_cart_link(self):
        self.click_on(loc.cart_modal_view_cart_link)

    # Checks
    @step
    def check_cart_modal_present(self):
        return self.check_element_visible(loc.cart_modal)
