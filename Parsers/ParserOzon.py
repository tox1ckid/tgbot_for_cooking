import time

import pyshorteners
from fake_useragent import UserAgent
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def short_url(url):
    return pyshorteners.Shortener().clckru.short(url)

def get_random_chrome_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random

def init_webdriver():
    driver = webdriver.Chrome()
    ua = get_random_chrome_user_agent()
    stealth(driver, user_agent=ua, languages=["ru", "en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.maximize_window()
    return driver


def get_products_links(item_name):
    driver = init_webdriver()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)
    find_input.send_keys(Keys.ENTER)

    product_link = ""
    try:
        product_link = short_url(driver.current_url)
    except:
        raise IOError("Something went wrong while parsing ozon.ru")

    driver.close()
    driver.quit()
    return product_link
