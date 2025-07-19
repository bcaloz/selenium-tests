from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
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
    UPLOAD_SUCCESS_TEXT = (By.XPATH, "//p[contains(text(), '.txt')]") # CHECK THIS

    def open(self) -> None:
        print("[FileUploadPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def upload_file(self, file_path: str):
        self._wait_for_element(self.FILE_INPUT).send_keys(file_path)

    def get_uploaded_filename(self) -> str:
        full_path = self._wait_for_element(self.FILE_INPUT).get_attribute("value")
        return os.path.basename(full_path)

    def click_upload_button(self):
        self._wait_for_element(self.UPLOAD_BUTTON).click()

    def assert_upload_success(self, filename: str):
        body_text = self._wait_for_element(self.UPLOAD_SUCCESS_TEXT).text
        self.assert_startswith(filename.split('_')[0], body_text, "Success message should include uploaded filename: ")
    
    def _wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))
    
# valid file upload + filename populates
# too large error + dismiss error
# selecting file + refresh page clears field