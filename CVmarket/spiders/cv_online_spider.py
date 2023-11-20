import scrapy
from urllib.parse import urljoin
import time


class QuotesSpider(scrapy.Spider):
    name = "cv_online_link_spider"
    start_urls = ["https://www.cvonline.lt/lt/categories"]

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

    def parse_link(self, response):
        url_general = response.meta["general_url"]
        # try:
        #    page = response.meta["page"]
        # except:
        #    page = "first_page"

        time.sleep(5)
        for item in response.css("li.vacancies-list__item.false"):
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
            city = item.css("div.jsx-3024910437 .vacancy-item__locations::text").get()

            yield {
                # "np": page,
                "url": url_general,
                "link": href,
                "description": description,
                "company": company,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "salary_type": "Prieš mokesčius",
                "city": city,
            }


#
# salary_from = item.css("div.salary-block::attr(data-salary-from)").get()
# salary_to = item.css("div.salary-block::attr(data-salary-to)").get()
# salary_type = item.css("span.salary-type::text").get()
# city = item.css("span.bg-blue-50 div::text").get()

# yield {
#    #"np": page,
#    "url": url_general,
#    "link": href,
#    "description": description,
#    "company": company,
#    "salary_from": salary_from,
#    "salary_to": salary_to,
#    "salary_type": salary_type,
#    "city": city,
# }

# next_page = response.xpath(
#    "/html/body/section/main/div[1]/div/ul/li[10]/a/@href"
# ).get()

# next_page_url = urljoin(url_general, next_page)
# print(next_page_url)
# if next_page:
#    yield scrapy.Request(
#        url=next_page_url,
#        callback=self.parse_link,
#        meta={"general_url": url_general, "page": next_page},
#    )

# yield {"name": name, "url": url, "category_id": category_id}


# scrapy crawl cv_online_link_spider -o output2.json
# scrapy crawl cv_online_link_spider -o cvonline_category.json