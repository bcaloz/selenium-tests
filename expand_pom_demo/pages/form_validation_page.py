from typing import Final
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from expand_pom_demo.pages.base_page import BasePage

class FormValidationPage(BasePage):
    """
    Page Object Model for https://practice.expandtesting.com/form-validation

    This page contains a multi-field form used to test front-end form validation.
    It includes:
    - Text input fields (name, contact number)
    - A date picker input
    - A dropdown for payment method
    - A register button
    - Field-level validation messages

    This class provides methods for interacting with and validating each of these elements.
    """

    # Locators
    URL: Final[str] = "https://practice.expandtesting.com/form-validation"
    PAGE_TITLE = (By.XPATH, "//h1[text()='Form Validation page for Automation Testing Practice']")

    # Functions
    def open(self) -> None:
        print("[FormValidationPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def _wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))