from pages.login_page import LoginPage
from settings import URL, User


class TestLogin:
    def test_login_positive(self, driver):
        email = User.MAIL
        password = User.PASSWORD

        login_page = LoginPage(driver)
        login_page.go_to(URL.MAIN + URL.LOGIN)
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        assert login_page.check_login_successful(), f"User {email} has not logged in"

    def test_login_invalid_credentials(self, driver):
        email = User.MAIL
        password = "wrong"

        login_page = LoginPage(driver)
        login_page.go_to(URL.MAIN + URL.LOGIN)
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        assert login_page.check_warning_present(), f"Login warning is not present"

