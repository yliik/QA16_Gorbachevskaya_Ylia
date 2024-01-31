import pytest
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver


@pytest.fixture(autouse=True)
def driver_chrome():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.21vek.by")
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture(autouse=True)
def handle_cookie(driver_chrome):
    try:
        cookie_overlay = driver_chrome.find_element(By.XPATH, '//*[@id="modal-cookie"]/div')
        if cookie_overlay:
            accept_button = cookie_overlay.find_element(By.XPATH,
                                                        '//*[@id="modal-cookie"]/div/div[2]/div[2]/button[2]/div')
            accept_button.click()
    except Exception as e:
        print(f"Error handling cookies: {e}")