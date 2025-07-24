import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from main_pom_project.pages.file_download_page import FileDownloadPage
from conftest import wait_for_file


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
def test_file_downloads_successfully(driver: WebDriver) -> None:
    """
    Click download link for 'some-file.txt' and verify the file
    was successfully downloaded.
    """
    page = FileDownloadPage(driver)
    page.open()

    # Click link to trigger download
    page.click_download_link()

    # This is dynamically added in the fixture
    download_file_path = driver.download_dir / "some-file.txt"  # type: ignore[attr-defined]
    assert wait_for_file(download_file_path), f"File not found: {download_file_path}"
