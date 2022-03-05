import platform
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

platform_s = platform.system()

if platform_s == 'Darwin':
    BROWSER_DRIVER_PATH = "./driver/chromedriver_mac"
elif platform_s == 'Linux':
    BROWSER_DRIVER_PATH = "./driver/chromedriver_linux"
else:
    BROWSER_DRIVER_PATH = "./driver/chromedriver_win.exe"


def take_screen(panel_url: str) -> bytes:

    print(panel_url)

    browser_options = webdriver.ChromeOptions()

    browser_options.add_argument("--headless")
    browser_options.add_argument("--disable-gpu")
    browser_options.add_argument("--disable-dev-shm-usage")
    browser_options.add_argument("no-sandbox")
    browser_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        executable_path=BROWSER_DRIVER_PATH,
        chrome_options=browser_options
    )

    driver.set_window_size(1920, 1080)

    driver.get('https://grafana.vkoro.ru/login')

    try:

        login_input = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//input[@name="user"]'))
        )

        login_input.send_keys(
            os.getenv('GF_LOGIN')
        )

        pwd_input = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//input[@name="password"]'))
        )

        pwd_input.send_keys(
            os.getenv('GF_PASSWORD')
        )

        pwd_input = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//button[@aria-label="Login button"]'))
        )

        pwd_input.click()

        assert WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//img[@alt="admin logo"]')
            )
        )

        driver.get(panel_url)

        assert WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="react-grid-layout"]')
            )
        )

        assert WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//canvas')
            )
        )

        return driver.get_screenshot_as_png()

    except Exception as e:
        print(e)

        driver.quit()
