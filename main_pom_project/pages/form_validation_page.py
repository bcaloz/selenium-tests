from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from main_pom_project.pages.base_page import BasePage


class FormValidationPage(BasePage):
    """
    Page Object Model for
    https://practice.expandtesting.com/form-validation

    This page contains a multi-field form used to test front-end form
    validation.

    It includes:
    - Text input fields (name, contact number)
    - A date picker input
    - A dropdown for payment method
    - A register button
    - Field-level validation messages

    This class provides methods for interacting with and validating
    each of these elements.
    """

    URL = "https://practice.expandtesting.com/form-validation"
    PAGE_TITLE = (
        By.XPATH,
        "//h1[text()='Form Validation page for Automation Testing Practice']",
    )
    NAME_INPUT = (By.ID, "validationCustom01")
    NAME_ERROR_MSG = (
        By.XPATH,
        "//input[@id='validationCustom01']/following-sibling::div[contains(@class, 'invalid-feedback')]",
    )
    NAME_SUCCESS_MSG = (
        By.XPATH,
        "//input[@id='validationCustom01']/following-sibling::div[contains(@class, 'valid-feedback')]",
    )
    PHONE_INPUT = (By.NAME, "contactnumber")
    PHONE_ERROR_MSG = (
        By.XPATH,
        "//input[@id='validationCustom05']/following-sibling::div[contains(@class, 'invalid-feedback')]",
    )
    DATE_INPUT = (By.NAME, "pickupdate")
    DATE_ERROR_MSG = (
        By.XPATH,
        "//input[@name='pickupdate']/following-sibling::div[contains(@class, 'invalid-feedback')]",
    )
    PAYMENT_SELECT = (By.ID, "validationCustom04")
    PAYMENT_ERROR_MSG = (
        By.XPATH,
        "//select[@id='validationCustom04']/parent::div/div[contains(@class, 'invalid-feedback')]",
    )
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-primary")
    CONFIRM_MSG = (By.CSS_SELECTOR, "div.alert.alert-info > p")

    def open(self) -> None:
        print("[FormValidationPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def fill_form(self, name: str, phone: str, date: str, payment_method: str) -> None:
        self._input_text(self.NAME_INPUT, name)
        self._input_text(self.PHONE_INPUT, phone)
        self._input_text(self.DATE_INPUT, date)
        self._select_dropdown(self.PAYMENT_SELECT, payment_method)

    def click_register_button(self) -> None:
        self._wait_for_element(self.REGISTER_BUTTON).click()

    def get_confirmation_message(self) -> str:
        return self._wait_for_element(self.CONFIRM_MSG).text.strip()

    def clear_name_field(self) -> None:
        elem = self._wait_for_element(self.NAME_INPUT)
        elem.clear()

    def get_name_error_msg(self) -> str:
        return self._wait_for_element(self.NAME_ERROR_MSG).text.strip()

    def get_name_success_msg(self) -> str:
        return self._wait_for_element(self.NAME_SUCCESS_MSG).text.strip()

    def get_phone_error_msg(self) -> str:
        return self._wait_for_element(self.PHONE_ERROR_MSG).text.strip()

    def get_phone_success_indicator(self) -> bool:
        return self._element_is_hidden(self.PHONE_ERROR_MSG)

    def get_date_error_msg(self) -> str:
        return self._wait_for_element(self.DATE_ERROR_MSG).text.strip()

    def get_date_success_indicator(self) -> bool:
        return self._element_is_hidden(self.DATE_ERROR_MSG)

    def get_payment_error_msg(self) -> str:
        return self._wait_for_element(self.PAYMENT_ERROR_MSG).text.strip()

    def get_payment_success_indicator(self) -> bool:
        return self._element_is_hidden(self.PAYMENT_ERROR_MSG)

    def _input_text(self, locator: tuple[str, str], text: str) -> None:
        elem = self._wait_for_element(locator)
        elem.clear()
        elem.send_keys(text)

    def _select_dropdown(self, locator: tuple[str, str], visible_text: str) -> None:
        from selenium.webdriver.support.ui import Select

        select = Select(self._wait_for_element(locator))
        select.select_by_visible_text(visible_text)
