import scrapy
import time
import sys
from scrapy.http import HtmlResponse
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# selenium_logger.setLevel(logging.WARNING)
logging.getLogger("scrapy").setLevel(logging.ERROR)
logging.getLogger("selenium.webdriver").setLevel(logging.ERROR)
logging.getLogger("websockets.protocol").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

sys.path.append("./Selenium/")
from scraping_engine import ScrapingEngine
from selenium.webdriver.common.by import By


class QuotesSpider(scrapy.Spider):
    name = "cv_online_link_spider"
    start_urls = ["https://www.cvonline.lt/lt/categories"]
    selenium_engine = ScrapingEngine()

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.parse_function = kwargs.get("parse_function", "parse")

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

    def __close_pop_up(self, engine):
        try:
            close = self.selenium_engine.driver.find_element(
                By.CSS_SELECTOR,
                "button[type='button'].jsx-4189752321.close-modal-button",
            )
            if close:
                close.click()
        except:
            pass
        time.sleep(5)
        try:
            cookies = self.selenium_engine.driver.find_element(
                By.CLASS_NAME, "cookie-consent-button"
            )
            if cookies:
                cookies.click()
        except:
            pass

    def parse_category(self, response):
        for a_element in response.css(
            "div.jsx-3492702657.categories__vacancy_categories a"
        ):
            link = a_element.css("a::attr(href)").get()
            name = a_element.css("a::text").get()
            yield {"name": name, "url": link}

    def parse(self, response):
        for a_element in response.css(
            "div.jsx-3492702657.categories__vacancy_categories a"
        ):
            link = a_element.css("a::attr(href)").get()
            name = a_element.css("a::text").get()
            # yield {"name": name, "url": link}
            full_url = response.urljoin(link)
            print("!!!!!!!!! ČIA PARSE FUNKCIJA RENKA DUOMENYS !!!!!!!!!!!!!!!!!!!")
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_link,
                meta={"name": name, "general_url": full_url},
            )

    def parse_link(self, response):
        url_general = response.meta["general_url"]
        self.selenium_engine.driver.execute_script("window.open('', '_blank');")

        # Przejdź do ostatniej otwartej zakładki
        self.selenium_engine.driver.switch_to.window(
            self.selenium_engine.driver.window_handles[-1]
        )

        self.selenium_engine.driver.get(response.url)
        time.sleep(5)
        self.__close_pop_up(engine=self.selenium_engine.driver)

        html_source = self.selenium_engine.driver.page_source

        time.sleep(5)

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
            try:
                next_page = self.selenium_engine.driver.find_element(
                    By.CSS_SELECTOR, "button[aria-label='Next']"
                )
                print("!!!!SURASTAS NEXT MYGTUKAS!!!!")
            except:
                next_page = False
                print("???????????NESURASTAS NEXT MYGTUKAS???????????????????")

            if next_page:
                if next_page and not next_page.get_attribute("disabled"):
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(next_page)
                    next_page.click()
                    print(
                        f"!!!!!!!!!!Laukimas prieš nusiuniant response!!!!!!!!!!!!!!!"
                    )
                    time.sleep(10)
                    page += 1
                    print(f"!!!!!!!!!!NUSPAUSTAS NEXT MYGTUKAS {page} PUSLAPIS")
                    new_response = HtmlResponse(
                        url=self.selenium_engine.driver.current_url,
                        body=self.selenium_engine.driver.page_source,
                        encoding="utf-8",
                    )
                else:
                    print(
                        "??????????CIKLAS NUTRAUKTAS dėl neaktyvaus mygtuko???????????????"
                    )
                    break
            else:
                print(
                    "??????????CIKLAS NUTRAUKTAS nes nesurastas mygtukas???????????????"
                )
                break

        self.selenium_engine.driver.execute_script("window.open('', '_blank');")

        # Przejdź do ostatniej otwartej zakładki
        self.selenium_engine.driver.switch_to.window(
            self.selenium_engine.driver.window_handles[-1]
        )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, getattr(self, self.parse_function, self.parse))


# scrapy crawl cv_online_link_spider -o ./output/cvonline.json
# scrapy crawl cv_online_link_spider -o ./output/cvonline_category.json -a parse_function=parse_category
