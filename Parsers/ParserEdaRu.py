import math
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

confusing = {"стак": {"value": 250, "type": "мл"}, "чайн": {"value": 5, "type": "мл"},
             "стол": {"value": 15, "type": "мл"}}


def get_random_chrome_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random


def init_webdriver():
    driver = webdriver.Chrome()
    ua = get_random_chrome_user_agent()
    stealth(driver, user_agent=ua, languages=["ru", "en-US", "en"], vendor="Google Inc.", platform="Win32",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.maximize_window()
    return driver


def find_dish_on_website(name='zxc'):  # returns [portions, ingredients, measurements]
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
        if (len(products_urls) <= 1):
            return [0, 0]
        my_link = products_urls[2 if len(products_urls) > 2 else 1]
    except:
        raise IOError("Something went wrong while parsing eda.ru")

    driver.get(url=my_link)
    paths_of_ingredients = driver.find_elements(By.XPATH, "//span[@itemprop='recipeIngredient']")
    paths_of_measure = driver.find_elements(By.CLASS_NAME, 'emotion-bsdd3p')
    path_of_division = driver.find_element(By.CLASS_NAME, 'emotion-1047m5l')
    ingredients = [f'{link.text}' for link in paths_of_ingredients]  # ингредиенты
    measure = [link.text.split(' ') for link in paths_of_measure]  # типа граммовки
    division = path_of_division.text  # порций кол-во

    for i in range(len(measure)):
        changing = measure[i].copy()

        if (len(changing) == 0):
            raise IOError("0 info about measure")

        if (len(changing) == 1):  # case что-то плохое
            changing[0] = "по вкусу"
            measure[i] = changing
            continue

        if (changing[0] == "по"):  # case "по вкусу"
            continue

        tries = 0
        while (((len(str(changing[0]))) != 0) and (
                not changing[0].isnumeric())):  # удаляем непонятные символы на конце числа
            changing[0] = changing[0][:-1]
            tries += 1

        changing[0] = int(changing[0])

        if (tries > 0):
            if (len(str(changing[0])) == 0):  # corner case
                changing[0] = 0
            changing[0] += 1  # TODO обрабатывать как 1/4 1/2 3/4

        for name in confusing.keys():  # меняем типы данных
            if (name in changing[1]):
                changing[0] = confusing[name]['value'] * changing[0]
                changing[1] = confusing[name]['type']

                while (len(changing) > 2):  # "n чайных ложек бла блу бло" -> "n мл"
                    changing.pop()

        changing[0] = changing[0] / int(division)  # нормируем по кол-ву порций
        measure[i] = changing

    driver.close()
    driver.quit()
    return [ingredients, measure]


def calculate(portions, measure):
    for i in range(len(measure)):
        if (isinstance(measure[i][0], float)):
            measure[i][0] = math.ceil(float(portions) * measure[i][0])

    return measure
