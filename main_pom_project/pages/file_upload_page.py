import os
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from main_pom_project.pages.base_page import BasePage

class FileUploadPage(BasePage):
    """
    Page Object Model for https://practice.expandtesting.com/upload
    
    This page contains a file upload form used to test front-end file handling validation.
    It includes:
    - A file input field with a 500KB size limit
    - An upload button
    - Filename display on valid selection
    - Upload success message
    - Dismissable tooltip alert if no file selected (coverage excluded due to native browser tooltip limitation)

    This class provides methods for interacting with and validating each of these elements.
    """
    URL = "https://practice.expandtesting.com/upload"
    PAGE_TITLE = (By.XPATH, "//h1[text()='File Uploader page for Automation Testing Practice']")
    FILE_INPUT = (By.ID, "fileInput")
    UPLOAD_BUTTON = (By.ID, "fileSubmit")
    UPLOAD_SUCCESS_HEADER = (By.TAG_NAME, "h1")
    UPLOAD_SUCCESS_MESSAGE = (By.ID, "uploaded-files")

    def open(self) -> None:
        print("[FileUploadPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def upload_file(self, file_path: str):
        self._wait_for_element(self.FILE_INPUT).send_keys(file_path)

    def get_uploaded_filename(self) -> str:
        full_path: Optional[str] = self._wait_for_element(self.FILE_INPUT).get_attribute("value")
        # Resolve Pylance warning by checking if type is None
        if full_path is None:
            raise ValueError("Expected file input to contain a value.")
        # full_path will contain something like 'C:\\fakepath\\{file_name.txt}', so we extract only the file name
        return os.path.basename(full_path)

    def verify_uploaded_filename(self, expected_file_name: str) -> None:
        actual_file_name = self.get_uploaded_filename()
        self.assert_equal(expected_file_name, actual_file_name, "Filename should populate in file input field: ")

    def click_upload_button(self):
        self._wait_for_element(self.UPLOAD_BUTTON).click()

    def verify_upload_success(self, expected_file_name: str) -> None:
        expected_header = "File Uploaded!"
        actual_header = self._wait_for_element(self.UPLOAD_SUCCESS_HEADER).text
        self.assert_equal(expected_header, actual_header, "Upload success header mismatch: ")

        success_msg = self._wait_for_element(self.UPLOAD_SUCCESS_MESSAGE).text
        self.assert_in(expected_file_name, success_msg, "Uploaded filename not found in success message: ")

    def _wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))
    
# too large error + dismiss error
# selecting file + refresh page clears field