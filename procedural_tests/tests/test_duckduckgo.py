from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_duckduck_go_search():
    options = Options()
    # options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://duckduckgo.com/")

    search_box = driver.find_element(By.ID, "searchbox_input")
    search_box.send_keys("Test Automation")
    search_box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.title_contains("Test Automation"))
    assert "Test Automation" in driver.title
    driver.quit()
