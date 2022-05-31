import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

SELENOID = False


@pytest.fixture()
def driver(request):
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    if SELENOID:
        capabilities = {
            "browserName": "chrome",
            "version": "90.0",
            "screenResolution": "1920x1080x24",
            "sessionTimeout": "300s",
            "enableVNC": True,
        }
        driver = webdriver.Remote("http://localhost:8080//wd/hub", desired_capabilities=capabilities, options=options)
    else:
        # TODO use Service instead executable_path
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.maximize_window()

    yield driver

    # if request.node.rep_call.failed:
    #     allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)

    driver.quit()


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#     return rep