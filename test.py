from scraping_engine import ScrapingEngine
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException

import time

scrap = ScrapingEngine()


def _pop_up_closer():
    try:
        scrap.driver.find_element(
            scrap.By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
        ).click()

    except NoSuchElementException:
        print("Cookies pop up not found")
        pass
    try:
        scrap.driver.execute_script('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
    except JavascriptException:
        print("Pop up not found")
        pass
    time.sleep(3)


def get_cookies(url: str = "https://www.whoscored.com/") -> str("html file"):
    """Get cookies from url"""
    scrap.driver.get(url)
    _pop_up_closer()
    time.sleep(120)
    scrap.driver.quit()
    print("Cookies save")


if "__main__" == __name__:
    get_cookies()
