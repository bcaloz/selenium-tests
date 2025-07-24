import pytest
from pathlib import Path
from selenium import webdriver
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(temp_path: Path) -> Generator[WebDriver, None, None]:
    # Create a temp directory for downloads
    download_dir = temp_path / "downloads"
    download_dir.mkdir()

    chrome_prefs: dict[str, object] = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    options = Options()
    options.add_experimental_option("prefs", chrome_prefs)
    # options.add_argument("--headless")  # Uncomment if needed

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.download_dir = download_dir  # type: ignore[attr-defined]

    yield driver
    driver.quit()
