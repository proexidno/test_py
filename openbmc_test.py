from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import os
import time

load_dotenv()

OBMC_USERNAME = os.getenv("OBMC_USERNAME", "root")
OBMC_PASSWORD = os.getenv("OBMC_PASSWORD", "0penBmc")


def setup_driver():
    options = Options()
    driver = webdriver.Firefox(options=options)
    return driver


def test_successful_login():
    driver = setup_driver()
    try:
        driver.get("https://127.0.0.1:2443/#/login")
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-test-id='login-button-submit']"
        )

        username.send_keys(OBMC_USERNAME)
        password.send_keys(OBMC_PASSWORD)
        login_button.click()

        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "main-content"))
        )
        print("Тест 1: Успешная авторизация")
    except Exception as e:
        print("Тест 1: Ошибка при авторизации:", e)
    finally:
        driver.quit()


def test_invalid_login():
    driver = setup_driver()
    try:
        driver.get("https://127.0.0.1:2443/#/login")
        initial_url = driver.current_url

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-test-id='login-button-submit']"
        )

        username.send_keys(OBMC_USERNAME)
        password.send_keys(f"{OBMC_PASSWORD}WRONGPASS")
        login_button.click()

        time.sleep(1)

        if driver.current_url == initial_url:
            print("Тест 2, Успешен: Авторизация с неверными данными")
        else:
            print("Тест 2, Неуспешен: Авторизация с неверными данными")

    except Exception as e:
        print("Тест 2: Ошибка:", e)
    finally:
        driver.quit()


def test_DOS_login():
    driver = setup_driver()
    driver.get("https://127.0.0.1:2443/#/login")
    for _ in range(5):

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-test-id='login-button-submit']"
        )

        username.send_keys(OBMC_USERNAME)
        password.send_keys(f"{OBMC_PASSWORD}WRONGPASS")
        login_button.click()
        time.sleep(5)

    time.sleep(3)

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(
        By.CSS_SELECTOR, "button[data-test-id='login-button-submit']"
    )

    username.send_keys(OBMC_USERNAME)
    password.send_keys(f"{OBMC_PASSWORD}")
    login_button.click()
    print("Тест 3, успешен: Пользователь заблокирован")
    time.sleep(5)
    driver.quit()


test_successful_login()
test_invalid_login()
test_DOS_login()
