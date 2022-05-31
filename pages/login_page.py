from allure_commons._allure import step

from pages.base_page import BasePage
from locators import login_locators as loc


class LoginPage(BasePage):
    @property
    def username(self):
        return self.get_text(loc.username)

    @username.setter
    def username(self, username):
        self.enter_text(loc.username, username)

    @property
    def password(self):
        return self.get_text(loc.password)

    @password.setter
    def password(self, password):
        self.enter_text(loc.password, password)

    def login(self):
        self.click_on(loc.login_button)
