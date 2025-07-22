import os
import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from main_pom_project.pages.file_download_page import FileDownloadPage
from main_pom_project.utils import get_test_file_path


@pytest.mark.file_download
def test_page_title_is_correct(driver: WebDriver) -> None:
    """
    Ensure that the file download page loads correctly and the
    expected title is present.
    """
    page = FileDownloadPage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "File Downloader page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")


@pytest.mark.file_download
@pytest.mark.smoke
def test_file_download(driver: WebDriver) -> None:
    """
    Click download link for 'some-file.txt' and verify the file
    was successfully downloaded to the test_data folder.
    """
    page = FileDownloadPage(driver)
    page.open()

    # Click link to trigger download
    page.click_download_link()

    # Build local path and wait briefly for download
    local_file_path, _ = get_test_file_path("some-file.txt", __file__)
    time.sleep(1.5)  # adjust if download is slow

    # Validate file was downloaded
    file_exists = os.path.exists(local_file_path)
    page.assert_equal(
        True, file_exists, "Downloaded file not found in test_data folder: "
    )
