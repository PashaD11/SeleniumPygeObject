from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from settings import URL, User


class TestLogin:
    def test_login_positive(self, driver):
        login_page = LoginPage(driver)
        login_page.go_to(URL)
        login_page.username = User.STANDART
        login_page.password = User.STANDART_PASS
        login_page.login()

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_peek_present, "Login failed"
