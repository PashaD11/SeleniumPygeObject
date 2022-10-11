from helpers.step import step
from pages.base_page import BasePage
from locators import login_locators as loc


class LoginPage(BasePage):
    @step
    def get_username(self):
        return self.get_text(loc.username)

    @step
    def enter_username(self, username):
        self.enter_text(loc.username, username)

    @step
    def get_password(self):
        return self.get_text(loc.password)

    @step
    def enter_password(self, password):
        self.enter_text(loc.password, password)

    @step
    def click_login_button(self):
        self.click_on(loc.login_button)
