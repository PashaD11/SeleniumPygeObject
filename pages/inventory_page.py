from allure_commons._allure import step

from pages.base_page import BasePage
from locators import inventory_locators as loc


class InventoryPage(BasePage):
    @property
    def title(self):
        return self.get_text(loc.title)

    @property
    def is_peek_present(self):
        return self.check_element_visible(loc.peek)
