from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(headless=True):
    """
    Initializes and returns a configured Selenium WebDriver instance.

    :param headless: Run browser in headless mode (default: True).
    :return: WebDriver instance.
    """
    chrome_options = Options()

    if headless:
        pass
        #chrome_options.add_argument("--headless")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
