from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from settings import URL, User


class TestLogin:
    def test_login_positive(self, driver):
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.go_to(URL)
        login_page.enter_username(User.STANDARD)
        login_page.enter_password(User.STANDARD_PASS)
        login_page.click_login_button()

        assert inventory_page.check_peek_present, "Login failed"
