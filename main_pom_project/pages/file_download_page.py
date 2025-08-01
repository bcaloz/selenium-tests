from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from main_pom_project.pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
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
        # Known site issue: dynamic ads can block this click — test passes if stepped through manually.
        link = self._wait_for_element(self.DOWNLOAD_LINK)
        ActionChains(self.driver).move_to_element(link).pause(0.2).click(link).perform()
