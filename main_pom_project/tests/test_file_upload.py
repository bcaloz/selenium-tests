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
    Happy path – upload a valid file (less than 500KB), ensure the
    filename appears in the input field, and confirm success messages
    are displayed.
    """
    page = FileUploadPage(driver)
    page.open()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_file_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", "sample_upload.txt")
    )

    # Upload file and verify filename is displayed
    expected_filename = os.path.basename(local_file_path)
    page.select_file_to_upload(local_file_path)
    page.verify_uploaded_filename(expected_filename)
    page.click_upload_button()

    # Verify success header and confirmation message
    page.verify_upload_success(expected_filename)


@pytest.mark.file_upload
def test_upload_file_too_large(driver: WebDriver) -> None:
    """
    Upload a file exceeding 500KB, validate that an error message
    appears, then dismiss the error and verify it disappears.
    """
    page = FileUploadPage(driver)
    page.open()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", "upload_too_large.txt")
    )

    page.select_file_to_upload(file_path)
    page.click_upload_button()

    # Validate error message is visible
    expected_error_msg = "File too large, please select a file less than 500KB"
    actual_error_msg = page.get_upload_error_message()
    page.assert_equal(
        expected_error_msg, actual_error_msg, "Too large file error message mismatch: "
    )

    page.dismiss_upload_error()
    page.verify_upload_error_dismissed()


@pytest.mark.file_upload
def test_uploaded_file_resets_after_refresh(driver: WebDriver) -> None:
    """
    Upload a valid file, confirm filename appears, refresh page,
    and verify the input field is reset to empty/default state.
    """
    page = FileUploadPage(driver)
    page.open()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", "sample_upload.txt")
    )
    expected_filename = os.path.basename(file_path)

    # Select file and verify name appears in input
    page.select_file_to_upload(file_path)
    page.verify_uploaded_filename(expected_filename)

    # Refresh page and verify filename input resets
    page.refresh()
    page.verify_uploaded_filename("")
