import configparser
import os
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService

# from selenium.common.exceptions import JavascriptException
# from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from selenium.common.exceptions import NoSuchElementException

# from bs4 import BeautifulSoup

# from random import randint

# import pickle
# import time
# from time import sleep


class ScrapingEngine(By):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "config.cfg")
    config.read(config_path)
    chrome_driver_path = config.get("selenium config", "driver_path")

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--headless")
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        self.options.add_argument(f"user-agent={self.user_agent}")

        chrome_service = ChromeService(executable_path=self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=chrome_service, options=self.options)
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.By = type("", (By,), {})


if "__main__" == __name__:
    # c = get_driver_download_endpoints()
    scr = ScrapingEngine()
