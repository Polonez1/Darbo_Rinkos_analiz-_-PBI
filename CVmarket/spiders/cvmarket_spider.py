import scrapy

import scrapy
import bs4


class QuotesSpider(scrapy.Spider):
    name = "cv_market_links_spider"
    start_urls = ["https://www.cvmarket.lt/darbas-pagal-kategorija"]

    def parse(self, response):
        n = 1
        for div_element in response.css("div.mb-1.text-slate-500.font-semibold"):
            link = div_element.css("a::attr(href)").get()
            name = div_element.css("a::text").get()
            category_id = n
            if link:
                full_url = response.urljoin(link)

                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_link,
                    meta={"name": name, "url": full_url, "category_id": category_id},
                )
                n = n + 1
            else:
                yield {"name": name, "url": link}

    def parse_link(self, response):
        name = response.meta["name"]
        url = response.meta["url"]
        category_id = response.meta["category_id"]

        for item in response.css("div.flex.flex-shrink.flex-auto.flex-grow"):
            href = item.css("div.main-info a::attr(href)").get()
            description = item.css(
                "h2.xl\\:text-xl.font-bold.mt-2.hover\\:underline::text"
            ).get()
            company = item.css("span.job-company.mr-5::text").get()

            salary_from = item.css("div.salary-block::attr(data-salary-from)").get()
            salary_to = item.css("div.salary-block::attr(data-salary-to)").get()
            salary_type = item.css("span.salary-type::text").get()

            yield {
                "category_id": category_id,
                "link": href,
                "description": description,
                "company": company,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "salary_type": salary_type,
            }

        # yield {"name": name, "url": url, "category_id": category_id}


# scrapy crawl cv_market_links_spider -o output.json
#
