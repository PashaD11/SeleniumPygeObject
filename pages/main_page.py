from allure_commons._allure import step

from pages.base_page import BasePage
from locators import main_locators as loc


class MainPage(BasePage):
    """
    Page Object for common elements such as:
    - navbar elements: Logo, My Account, Log Out buttons
    - modal windows' elements: Ok, Cancel, Close buttons
    - other common elements: Burger menu
    Usually other pages extends MainPage for getting access to common methods
    """
    # Actions

