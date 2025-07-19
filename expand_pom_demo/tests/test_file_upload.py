import pytest
import os
from expand_pom_demo.pages.file_upload_page import FileUploadPage
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.file_upload
def test_page_title_is_correct(driver: WebDriver) -> None:
    """Ensure that the file upload page loads correctly and the expected title is present."""
    page = FileUploadPage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "File Uploader page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")

@pytest.mark.file_upload
def test_valid_file_upload(driver: WebDriver) -> None:
    """
    Select a valid file (less than 500 KB), ensure the file name populates in the input field,
    and confirm successful upload with expected confirmation text.
    """
    page = FileUploadPage(driver)
    page.open()

    local_file_path = os.path.abspath("test_data/sample_upload.txt")
    page.upload_file(local_file_path)
    expected_file_name = os.path.basename(local_file_path)
    actual_file_name = page.get_uploaded_filename()
    page.assert_equal(expected_file_name, actual_file_name, "Filename should populate in file input field: ")

    page.click_upload_button()
    #confirm redirection