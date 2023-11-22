import scrapy
from urllib.parse import urljoin
import time
import sys
from scrapy.http import HtmlResponse

sys.path.append("./Selenium/")
from scraping_engine import ScrapingEngine
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class QuotesSpider(scrapy.Spider):
    name = "cv_online_link_spider"
    start_urls = ["https://www.cvonline.lt/lt/categories"]
    selenium_engine = ScrapingEngine()

    def parse(self, response):
        for a_element in response.css(
            "div.jsx-3492702657.categories__vacancy_categories a"
        ):
            link = a_element.css("a::attr(href)").get()
            name = a_element.css("a::text").get()
            # yield {"name": name, "url": link}

            if link:
                full_url = response.urljoin(link)

                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_link,
                    meta={"name": name, "general_url": full_url},
                )
                break
            else:
                yield {"name": name, "url": link}

    def __salary_split(self, string: str, split_part: int):
        if string is None:
            return None
        else:
            new_string = string.partition("–")[split_part].replace("€", "").strip()
            return new_string

    def __city_split(self, string: str):
        if string is None:
            return None
        else:
            new_string = string.partition(",")[0].strip()
            return new_string

    def __close_pop_up(self):
        close = self.selenium_engine.driver.find_element(
            By.CSS_SELECTOR, "button[type='button'].jsx-4189752321.close-modal-button"
        )
        if close:
            close.click()
        time.sleep(5)
        cookies = self.selenium_engine.driver.find_element(
            By.CLASS_NAME, "cookie-consent-button"
        )
        if cookies:
            cookies.click()

    def parse_link(self, response):
        url_general = response.meta["general_url"]

        self.selenium_engine.driver.get(response.url)
        time.sleep(10)
        self.__close_pop_up()

        html_source = self.selenium_engine.driver.page_source

        time.sleep(10)

        new_response = HtmlResponse(
            url=self.selenium_engine.driver.current_url,
            body=html_source,
            encoding="utf-8",
        )
        page = 1
        while True:
            time.sleep(5)
            for item in new_response.css("li.vacancies-list__item.false"):
                href = item.css("div.jsx-3024910437 a::attr(href)").get()
                description = item.css(
                    "div.jsx-3024910437 span.jsx-3024910437.vacancy-item__title::text"
                ).get()
                company = item.css(
                    "div.jsx-3024910437 div.vacancy-item__body div.vacancy-item__column a::text"
                ).get()
                salary = item.css(
                    "div.jsx-3024910437 div.vacancy-item__info-secondary span.vacancy-item__salary-label::text"
                ).get()
                salary_from = self.__salary_split(salary, split_part=0)
                salary_to = self.__salary_split(salary, split_part=2)
                _city = item.css(
                    "div.jsx-3024910437 .vacancy-item__locations::text"
                ).get()
                city = self.__city_split(_city)

                yield {
                    "np": page,
                    "url": url_general,
                    "link": href,
                    "description": description,
                    "company": company,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "salary_type": "Prieš mokesčius",
                    "city": city,
                }

            next_page_xpath = '//*[@id="__next"]/div[2]/div[2]/div/div[2]/div/div/nav[1]/button[8]/svg/path'
            next_page = self.selenium_engine.driver.find_element(
                By.CSS_SELECTOR, "button[aria-label='Next']"
            )
            if next_page and not next_page.get_attribute("disabled"):
                next_page.click()
                time.sleep(5)
                page += 1
                new_response = HtmlResponse(
                    url=self.selenium_engine.driver.current_url,
                    body=self.selenium_engine.driver.page_source,
                    encoding="utf-8",
                )
            else:
                break

        time.sleep(10)
        self.selenium_engine.driver.close()


# scrapy crawl cv_online_link_spider -o output2.json
# scrapy crawl cv_online_link_spider -o cvonline_category.json
