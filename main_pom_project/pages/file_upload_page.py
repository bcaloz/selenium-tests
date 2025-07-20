import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from main_pom_project.pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class FileUploadPage(BasePage):
    """
    Page Object Model for https://practice.expandtesting.com/upload

    This page contains a file upload form used to test front-end file
    handling validation.

    It includes:
    - A file input field with a 500KB size limit
    - An upload button
    - Filename display on valid selection
    - Upload success message
    - Dismissable tooltip alert if no file selected (coverage excluded
      due to native browser tooltip limitation)

    This class provides methods for interacting with and validating
    each of these elements.
    """

    URL = "https://practice.expandtesting.com/upload"
    PAGE_TITLE = (
        By.XPATH,
        "//h1[text()='File Uploader page for Automation Testing Practice']",
    )
    FILE_INPUT = (By.ID, "fileInput")
    UPLOAD_BUTTON = (By.ID, "fileSubmit")
    UPLOAD_SUCCESS_HEADER = (By.TAG_NAME, "h1")
    UPLOAD_SUCCESS_MSG = (By.ID, "uploaded-files")
    UPLOAD_ERROR_MSG = (By.CSS_SELECTOR, "div.alert.alert-danger")
    UPLOAD_ERROR_DISMISS_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-close",
    )

    def open(self) -> None:
        print("[FileUploadPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def select_file_to_upload(self, file_path: str):
        self._wait_for_element(self.FILE_INPUT).send_keys(file_path)

    def get_uploaded_filename(self) -> str:
        # Ignore type error on get_attribute; None case is handled below
        full_path = self._wait_for_element(self.FILE_INPUT).get_attribute("value")  # type: ignore
        if full_path is None:
            raise ValueError("Expected file input to contain a value.")
        # full_path contains something like 'C:\\fakepath\\filename.txt';
        # extract only the file name
        return os.path.basename(full_path)

    def verify_uploaded_filename(self, expected_filename: str) -> None:
        actual_filename = self.get_uploaded_filename()
        self.assert_equal(
            expected_filename,
            actual_filename,
            "Filename should populate in file input field: ",
        )

    def click_upload_button(self) -> None:
        button = self._wait_for_element(self.UPLOAD_BUTTON)
        # Scroll just enough to trigger visibility in case element is hidden
        ActionChains(self.driver).move_to_element(button).pause(0.2).click(
            button
        ).perform()

    def verify_upload_success(self, expected_filename: str) -> None:
        expected_header = "File Uploaded!"
        actual_header = self._wait_for_element(self.UPLOAD_SUCCESS_HEADER).text
        self.assert_equal(
            expected_header, actual_header, "Upload success header mismatch: "
        )

        success_msg = self._wait_for_element(self.UPLOAD_SUCCESS_MSG).text
        self.assert_in(
            expected_filename,
            success_msg,
            "Uploaded filename not found in success message: ",
        )

    def get_upload_error_message(self) -> str:
        return self._wait_for_element(self.UPLOAD_ERROR_MSG).text.strip()

    def dismiss_upload_error(self) -> None:
        self._wait_for_element(self.UPLOAD_ERROR_DISMISS_BUTTON).click()

    def verify_upload_error_dismissed(self) -> None:
        self._wait_for_element_to_disappear(self.UPLOAD_ERROR_MSG)
        self.assert_equal(
            True,
            self._element_is_hidden(self.UPLOAD_ERROR_MSG),
            "Error message should no longer be visible after being dismissed: ",
        )

    def refresh(self) -> None:
        """Reload the current page."""
        self.driver.refresh()
        self._wait_for_element(self.PAGE_TITLE)
