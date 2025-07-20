import pytest
import os
from main_pom_project.pages.file_upload_page import FileUploadPage
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.file_upload
def test_page_title_is_correct(driver: WebDriver) -> None:
    """
    Ensure that the file upload page loads correctly and the
    expected title is present.
    """
    page = FileUploadPage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "File Uploader page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")


@pytest.mark.file_upload
@pytest.mark.smoke
def test_valid_file_upload(driver: WebDriver) -> None:
    """
    Select a valid file (less than 500 KB), ensure the file name
    populates in the input field, and confirm success messsages
    display after upload.
    """
    page = FileUploadPage(driver)
    page.open()

    # Resolve absolute path to sample_upload.txt in the test_data directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_file_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", "sample_upload.txt")
    )

    # Upload file, verify filename in input field, then click Upload
    expected_file_name = os.path.basename(local_file_path)
    page.upload_file(local_file_path)
    page.verify_uploaded_filename(expected_file_name)
    page.click_upload_button()

    # Verify success header and confirmation message
    page.verify_upload_success(expected_file_name)


@pytest.mark.file_upload
def test_upload_file_too_large(driver: WebDriver) -> None:
    """
    Upload a file exceeding 500KB, validate that an error message
    appears, then dismiss the error and verify it disappears.
    """
    page = FileUploadPage(driver)
    page.open()

    # Path to too-large file (e.g., upload_too_large.txt)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", "upload_too_large.txt")
    )

    page.upload_file(file_path)
    page.click_upload_button()

    # Validate error message is visible
    error_msg = page.get_upload_error_message()
    expected_msg = "File size exceeds maximum allowed limit of 500KB."
    page.assert_equal(
        expected_msg, error_msg, "Too large file error message mismatch: "
    )

    # Click the dismiss (X) button
    page.dismiss_upload_error()

    # Verify error is dismissed
    page.assert_upload_error_dismissed()


# selecting file + refresh page clears field
