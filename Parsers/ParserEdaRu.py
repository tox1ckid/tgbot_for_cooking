import time

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.maximize_window()
    return driver

def find_dish_on_website(name='zxc'): # returns [portions, ingredients, measurements]
    driver = init_webdriver()
    driver.get('https://eda.ru/recepty')
    driver.find_element(By.CLASS_NAME, 'emotion-rbn9vq').click()
    element = driver.find_element(By.NAME, 'input')
    element.clear()
    element.send_keys(name)
    time.sleep(2)
    element.send_keys(Keys.ENTER)
    driver.get(url=f'{driver.current_url}&onlyEdaChecked=true')
    time.sleep(2)

    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'emotion-18hxz5k')
        products_urls = list([f'{link.get_attribute("href")}' for link in find_links])
        if (len(products_urls) == 1):
            return ["Not enough recipes on the website", [], []]
        my_link = products_urls[2 if len(products_urls) > 2 else 1]
    except:
        raise IOError("Something went wrong while parsing eda.ru")

    driver.get(url=my_link)
    paths_of_ingredients = driver.find_elements(By.XPATH, "//span[@itemprop='recipeIngredient']")
    paths_of_measure = driver.find_elements(By.CLASS_NAME, 'emotion-bsdd3p')
    path_of_division = driver.find_element(By.CLASS_NAME, 'emotion-1047m5l')
    ingredients = [f'{link.text}' for link in paths_of_ingredients]
    measure = [link.text.split(' ') for link in paths_of_measure]
    division = path_of_division.text
    driver.close()
    driver.quit()
    return [division, ingredients, measure]

