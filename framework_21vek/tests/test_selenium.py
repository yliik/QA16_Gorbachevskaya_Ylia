import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


@pytest.fixture
def driver_chrome():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.21vek.by")
    yield driver
    driver.close()
    driver.quit()

@pytest.fixture
def handle_cookie(driver_chrome):
    try:
        cookie_overlay = driver_chrome.find_element(By.XPATH, '//*[@id="modal-cookie"]/div')
        if cookie_overlay:
            accept_button = cookie_overlay.find_element(By.XPATH,
                                                        '//*[@id="modal-cookie"]/div/div[2]/div[2]/button[2]/div')
            accept_button.click()
    except Exception as e:
        print(f"Error handling cookies: {e}")


def test_product_search(driver_chrome):
    search_box=driver_chrome.find_element(By.ID,"catalogSearch")
    search_box.send_keys("Телевизоры")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    assert driver_chrome.find_element(By.XPATH,"(//*[@class='b-recipes__item__link j-category__link'])[1]")


def test_navigate_to_shop_from_menu(driver_chrome):
    xpath = '//*[@id="header"]/div/div[4]/div/div/ul/li[3]/a'
    element = driver_chrome.find_element(By.XPATH, xpath)
    element.click()
    assert driver_chrome.title == 'Купить холодильник в Минске, холодильники в рассрочку - 21vek.by'
    assert driver_chrome.current_url == 'https://www.21vek.by/refrigerators/'


def test_adding_in_cart(driver_chrome,handle_cookie):
    xpath = '//*[@id="content"]/div[2]/section/div/div/div/div/div/div/div[1]/div/div/div[3]/div[3]/button/div'
    add_to_card = driver_chrome.find_element(By.XPATH, xpath)
    add_to_card.click()
    time.sleep(5)
    assert driver_chrome.find_element(By.XPATH,
                                      '//*[@id="header"]/div/div[3]/div/div[4]/a/span[1]/span')


def test_social_media_button(driver_chrome,handle_cookie):
    xpath = '//*[@id="footer-inner"]/div/div/div[3]/a[3]/div'
    instagram_button=driver_chrome.find_element(By.XPATH,xpath)
    time.sleep(5)
    instagram_button.click()
    time.sleep(10)
    driver_chrome.switch_to.window(driver_chrome.window_handles[-1])
    assert driver_chrome.current_url == 'https://www.instagram.com/21vek.by/'


def find_and_click_element(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()


def test_login_password(driver_chrome,handle_cookie):
    user_button_xpath = '//*[@id="header"]/div/div[3]/div/div[3]/div/div/div/button'
    user_button_dropdown_xpath = '//*[@id="userToolsDropDown"]/div/div[1]/div[2]/button'
    find_and_click_element(driver_chrome, user_button_xpath)
    time.sleep(2)
    find_and_click_element(driver_chrome, user_button_dropdown_xpath)
    time.sleep(2)
    login=driver_chrome.find_element(By.XPATH,'//*[@id="login-email"]')
    login.send_keys("juli.01071369@gmail.com")
    password = driver_chrome.find_element(By.XPATH, '//*[@id="login-password"]')
    password.send_keys("nupKub-5rovge-ruswyh")
    enter_button_xpath = '//*[@id="default-:R2m6:-modal"]/div/div/div[2]/div/div/form/div/div[3]/button'
    find_and_click_element(driver_chrome, enter_button_xpath)
    time.sleep(5)
    find_and_click_element(driver_chrome, user_button_xpath)
    assert driver_chrome.find_element(By.XPATH, '//*[@id="userToolsDropDown"]/div/span')