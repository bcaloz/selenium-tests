from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


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

    def scroll_to_bottom(self) -> None:
        ActionChains(self.driver).send_keys(Keys.END).perform()

    def _wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _wait_for_element_to_disappear(self, locator: tuple[str, str]) -> bool:
        result = WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(locator)
        )
        return bool(result)

    def _element_is_hidden(self, locator: tuple[str, str]) -> bool:
        try:
            elem = self.driver.find_element(*locator)
            return not elem.is_displayed()
        except Exception:
            return True  # If not found, treat as hidden

    @staticmethod
    def assert_equal(
        expected: object, actual: object, message_prefix: str = ""
    ) -> None:
        assert (
            expected == actual
        ), f"{message_prefix}Expected: '{expected}', Actual: '{actual}'"

    @staticmethod
    def assert_startswith(expected: str, actual: str, message_prefix: str = "") -> None:
        assert actual.startswith(
            expected
        ), f"{message_prefix}Expected start: '{expected}', Actual: '{actual}'"

    @staticmethod
    def assert_in(expected: str, actual: str, message_prefix: str = "") -> None:
        assert (
            expected in actual
        ), f"{message_prefix}Expected to find: '{expected}', in: '{actual}'"
