import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    opts = Options()
    # opts.add_argument("--headless")
    svc = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=svc, options=opts)
    yield drv
    drv.quit()