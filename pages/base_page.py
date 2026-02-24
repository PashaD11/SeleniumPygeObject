from typing import List, Callable

import pytest
from allure_commons._allure import step
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

EXPLICIT_TIMEOUT = 20


class BasePage:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @staticmethod
    def _get_text_from_element(element: WebElement):
        element_text = element.text
        if not element_text:
            element_text = element.get_attribute("value")
        if not element_text:
            element_text = element.get_property("value")
        return element_text

    @step
    def go_to(self, url):
        self.driver.get(url)

    @step
    def wait_element(self, locator: str, condition: Callable = ec.presence_of_element_located, timeout=EXPLICIT_TIMEOUT,
                     by=By.CSS_SELECTOR, parent=None) -> WebElement:
        if locator.startswith("//"):
            by = By.XPATH
        if not parent:
            parent = self.driver
        return WebDriverWait(parent, timeout).until(condition((by, locator)))

    @step
    def wait_all_elements(self, locator: str, condition: Callable = ec.presence_of_all_elements_located,
                          timeout=EXPLICIT_TIMEOUT, by=By.CSS_SELECTOR, parent=None) -> List[WebElement]:
        if locator.startswith("//"):
            by = By.XPATH
        if not parent:
            parent = self.driver
        return WebDriverWait(parent, timeout).until(condition((by, locator)))

    @step
    def click_on(self, locator: str, timeout=EXPLICIT_TIMEOUT, scroll=True, parent=None) -> WebElement:
        if not parent:
            parent = self.driver
        element = self.wait_element(locator, ec.element_to_be_clickable, timeout, parent=parent)
        if scroll:
            element.location_once_scrolled_into_view
        element.click()
        return element

    @step
    def click_in_list_by_text(self, locator_of_list: str, text: str, exact=True):
        # TODO need to check that element is clickable
        element_list = self.wait_all_elements(locator_of_list)
        for element in element_list:
            if exact:
                if self._get_text_from_element(element) == text:
                    element.click()
                    break
            else:
                if text in self._get_text_from_element(element):
                    element.click()
                    break
        else:
            pytest.fail(f"Cant find element with text - {text}")

    @step
    def click_in_list_by_num(self, locator_of_list: str, num: int, scroll=False):
        # TODO need to check that element is clickable
        element_list = self.wait_all_elements(locator_of_list, ec.visibility_of_all_elements_located)
        if scroll:
            element_list[num].location_once_scrolled_into_view
        element_list[num].click()

    def enter_text(self, locator: str, text: str, timeout=EXPLICIT_TIMEOUT):
        element = self.wait_element(locator, ec.element_to_be_clickable, timeout)
        element.clear()
        element.send_keys(text)

    def enter_input_value(self, locator: str, text: str, timeout=EXPLICIT_TIMEOUT):
        element = self.wait_element(locator, ec.presence_of_element_located, timeout)
        self.driver.execute_script(f"arguments[0].value = '{text}';", element)

    @step
    def select_option(self, locator, text_or_value=None, index=None):
        select = self.wait_element(locator)
        if index:
            Select(select).select_by_index(index)
            return
        else:
            try:
                Select(select).select_by_visible_text(text_or_value)
                return
            except NoSuchElementException:
                pass
            try:
                Select(select).select_by_value(text_or_value)
                return
            except NoSuchElementException:
                pass
            pytest.fail(f"Option with {text_or_value=} not found")

    @step
    def screenshot_page(self, file_name: str):
        self.driver.save_screenshot(file_name)
        return file_name

    @step
    def screenshot_element(self, locator: str, file_name: str, timeout=EXPLICIT_TIMEOUT) -> bool:
        return self.wait_element(locator, ec.visibility_of_element_located, timeout).screenshot(file_name)

    @step
    def switch_to_frame(self, locator: str, timeout=EXPLICIT_TIMEOUT) -> WebElement:
        return self.wait_element(locator, ec.frame_to_be_available_and_switch_to_it, timeout)

    @step
    def switch_to_main_frame(self):
        self.driver.switch_to.parent_frame()

    @step
    def wait_until_disappear(self, locator: str, visible_timeout=3, disappear_timeout=60, debug=False):
        try:
            self.wait_element(locator, ec.visibility_of_element_located, timeout=visible_timeout)
        except TimeoutException:
            if debug:
                print(f"Element {locator=} didn't appear")
            pass
        self.wait_element(locator, ec.invisibility_of_element_located, timeout=disappear_timeout)

    @step
    def switch_tab(self, num):
        self.driver.switch_to.window(self.driver.window_handles[num])

    @step
    def wait_page_load(self):
        WebDriverWait(self.driver, EXPLICIT_TIMEOUT).until(self.ec_wait_page_load)

    @step
    def refresh_page(self, wait_load_page=True):
        self.driver.refresh()
        if wait_load_page:
            self.wait_page_load()

    @step
    def confirm_alert(self):
        self.driver.switch_to.alert.accept()

    # GET:
    @step
    def get_text(self, locator: str, timeout=EXPLICIT_TIMEOUT, parent=None) -> str:
        if not parent:
            parent = self.driver
        element = self.wait_element(locator, ec.visibility_of_element_located, timeout=timeout, parent=parent)
        return self._get_text_from_element(element)

    @step
    def get_text_with_wait(self, locator: str, text: str, timeout=EXPLICIT_TIMEOUT, by=By.CSS_SELECTOR):
        if locator.startswith("//"):
            by = By.XPATH
        WebDriverWait(self.driver, timeout).until(ec.text_to_be_present_in_element((by, locator), text))
        return self.get_text(locator)

    @step
    def get_text_list(self, locator: str, timeout=EXPLICIT_TIMEOUT) -> List[str]:
        text_list = []
        try:
            element_list = self.wait_all_elements(locator, timeout=timeout)
        except TimeoutException:
            return []
        for element in element_list:
            text_list.append(self._get_text_from_element(element))
        return text_list

    @step
    def get_current_url(self):
        return self.driver.current_url

    @step
    def get_alert_message(self, timeout=EXPLICIT_TIMEOUT):
        try:
            alert = WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
            return alert.text
        except NoAlertPresentException:
            return False

    # CHECKS:
    @step
    def check_element_visible(self, locator: str, timeout=EXPLICIT_TIMEOUT):
        try:
            self.wait_element(locator, ec.visibility_of_element_located, timeout)
            return True
        except TimeoutException:
            return False

    @step
    def check_element_not_visible(self, locator: str, timeout=EXPLICIT_TIMEOUT):
        try:
            self.wait_element(locator, ec.invisibility_of_element_located, timeout)
            return True
        except TimeoutException:
            return False

    @step
    def check_element_clickable(self, locator: str, timeout=EXPLICIT_TIMEOUT):
        try:
            self.wait_element(locator, ec.element_to_be_clickable, timeout)
            return True
        except TimeoutException:
            return False

    # Expected Conditions
    @staticmethod
    def ec_wait_page_load(driver):
        load_state = driver.execute_script("return document.readyState")
        return load_state == "complete"
