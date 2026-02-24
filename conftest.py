import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.cart_page import CartPage
from settings import URL


@pytest.fixture()
def driver(request):
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.maximize_window()

    yield driver

    # if request.node.rep_call.failed:
    #     allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)

    driver.quit()

@pytest.fixture()
def empty_cart_after_test(driver):
    # there is no API methods for cart so the only way is through the UI
    yield
    # teardown
    cart_page = CartPage(driver)
    cart_page.go_to(URL.MAIN + URL.CART)
    cart_page.delete_all_products()


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#     return rep