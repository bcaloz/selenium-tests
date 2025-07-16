from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import Final

class BasePage:
    """
    Abstract base class for all Page Object Model (POM) classes.

    Provides shared functionality such as:
    - WebDriver instance and explicit waits
    - Common utility methods like element waiting and assertions

    All page objects should inherit from this class to maintain consistency
    and avoid code duplication across the framework.
    """
    TIMEOUT = 10

    def __init__(self, driver: WebDriver, timeout: int = TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    @staticmethod
    def assert_equal(expected: object, actual: object, message_prefix: str = "") -> None:
        assert expected == actual, f"{message_prefix}Expected: '{expected}', Actual: '{actual}'"

    @staticmethod
    def assert_startswith(expected: str, actual: str, message_prefix: str = "") -> None:
        assert actual.startswith(expected), f"{message_prefix}Expected start: '{expected}', Actual: '{actual}'"
