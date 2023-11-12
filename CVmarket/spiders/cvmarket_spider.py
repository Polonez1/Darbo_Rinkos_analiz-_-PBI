import scrapy

import scrapy
import bs4


class QuotesSpider(scrapy.Spider):
    name = "cv_market_links_spider"
    start_urls = ["https://www.cvmarket.lt/darbas-pagal-kategorija"]

    def parse(self, response):
        for div_element in response.css("div.mb-1.text-slate-500.font-semibold"):
            link = div_element.css("a::attr(href)").get()
            name = div_element.css("a::text").get()

            yield scrapy.Request(
                url=link, callback=self.parse_link, meta={"name": name}
            )

    def parse_link(self, response):
        name = response.meta["name"]

        yield {"name": name, "url": response.url}


# scrapy crawl cv_market_links_spider -o output.json
#
