from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def test_google_search():
    options = Options()
    #options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("ChatGPT")
    search_box.submit()

    assert "ChatGPT" in driver.title
    driver.quit()