from allure_commons._allure import step

from locators import login_locators as loc
from pages.main_page import MainPage
from settings import URL


class LoginPage(MainPage):
    # Actions
    @step
    def enter_email(self, email):
        self.enter_text(loc.email, email)

    # don't use @step as this reveal password in reports
    def enter_password(self, password):
        self.enter_text(loc.password, password)

    @step
    def click_login_button(self):
        self.click_on(loc.login_button)

    def sing_in(self, email, password):
        # use this method as a shortcut for quick sign-in in each test
        # it is an exception to use assert inside page object
        assert URL.MAIN, "Main URL not found. Perhaps environment variables hasn't been set?"
        self.go_to(URL.MAIN)
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        assert self.check_login_successful(), f"Customer {email} has not signed in"

    # Checks
    @step
    def check_login_successful(self):
        return self.check_element_visible(loc.user_icon)
