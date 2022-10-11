from helpers.step import step
from pages.base_page import BasePage
from locators import inventory_locators as loc


class InventoryPage(BasePage):
    # Actions
    @step
    def open_item_by_name(self, name):
        self.click_in_list_by_text(loc.item_name_list, name)

    # Reads
    @step
    def get_title(self):
        return self.get_text(loc.title)

    # Checks
    @step
    def check_peek_present(self):
        return self.check_element_visible(loc.peek)
