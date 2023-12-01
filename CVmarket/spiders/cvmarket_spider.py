import scrapy
from urllib.parse import urljoin
import time


class QuotesSpider(scrapy.Spider):
    name = "cv_market_links_spider"
    start_urls = ["https://www.cvmarket.lt/darbas-pagal-kategorija"]

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.parse_function = kwargs.get("parse_function", "parse")

    def parse_category(self, response):
        for div_element in response.css("div.mb-1.text-slate-500.font-semibold"):
            link = div_element.css("a::attr(href)").get()
            name = div_element.css("a::text").get()
            yield {"name": name, "url": link}

    def parse(self, response):
        for div_element in response.css("div.mb-1.text-slate-500.font-semibold"):
            link = div_element.css("a::attr(href)").get()
            name = div_element.css("a::text").get()
            if link:
                full_url = response.urljoin(link)

                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_link,
                    meta={"name": name, "general_url": full_url},
                )
            else:
                yield {"name": name, "url": link}

    def parse_link(self, response):
        url_general = response.meta["general_url"]
        try:
            page = response.meta["page"]
        except:
            page = "first_page"

        time.sleep(5)
        for item in response.css(
            "div.lg\\:container section.flex.flex-col article.flex-col.lg\\:flex-row"
        ):
            href = item.css("div.main-info a::attr(href)").get()
            description = item.css(
                "h2.xl\\:text-xl.font-bold.mt-2.hover\\:underline::text"
            ).get()
            company = item.css("span.job-company.mr-5::text").get()

            salary_from = item.css("div.salary-block::attr(data-salary-from)").get()
            salary_to = item.css("div.salary-block::attr(data-salary-to)").get()
            salary_type = item.css("span.salary-type::text").get()
            city = item.css("span.bg-blue-50 div::text").get()

            yield {
                "np": page,
                "url": url_general,
                "link": href,
                "description": description,
                "company": company,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "salary_type": salary_type,
                "city": city,
            }

        next_page = response.xpath(
            "/html/body/section/main/div[1]/div/ul/li[10]/a/@href"
        ).get()

        next_page_url = urljoin(url_general, next_page)
        print(next_page_url)
        if next_page:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_link,
                meta={"general_url": url_general, "page": next_page},
            )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, getattr(self, self.parse_function, self.parse))

        # yield {"name": name, "url": url, "category_id": category_id}


# scrapy crawl cv_market_links_spider -o ../output/cvmarket.json
# scrapy crawl cv_market_links_spider -o ./output/cvmarket_category.json -a parse_function=parse_category
