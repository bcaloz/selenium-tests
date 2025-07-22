from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from main_pom_project.pages.base_page import BasePage
import os
from main_pom_project.utils import get_test_file_path


class FileDownloadPage(BasePage):
    """
    Page Object Model for https://practice.expandtesting.com/download

    This page provides static file links used to test browser-based
    file download functionality.

    It includes:
    - A list of downloadable files (e.g. .txt, .png, .json)
    - Download links triggering direct browser downloads

    This class provides methods for validating page load and verifying
    that file downloads complete successfully.
    """

    URL = "https://practice.expandtesting.com/download"
    PAGE_TITLE = (
        By.XPATH,
        "//h1[text()='File Downloader page for Automation Testing Practice']",
    )
    DOWNLOAD_LINK = (By.CSS_SELECTOR, 'a[data-testid="some-file.txt"]')

    def open(self) -> None:
        print("[FileDownloadPage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def click_download_link(self) -> None:
        self.scroll_to_bottom()
        self._wait_for_element(self.DOWNLOAD_LINK).click()

    def verify_file_was_downloaded(self, filename: str, download_dir: str) -> None:
        local_file_path, _ = get_test_file_path("some-file.txt", __file__)
        self.assert_equal(
            True,
            os.path.exists(local_file_path),
            f"Expected file '{filename}' to exist in '{download_dir}', but it was not found.",
        )
