import scrapy
from urllib.parse import urljoin


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
                    meta={
                        "name": name,
                        "general_url": full_url,
                        "category_id": category_id,
                    },
                )
                n = n + 1
                break
            else:
                yield {"name": name, "url": link}

    def parse_link(self, response):
        url_general = response.meta["general_url"]
        np = response.css("div.lg\\:container a.flex.rounded-full::attr(href)").get()

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
                "np": np,
                "url_general": url_general,
                "link": href,
                "description": description,
                "company": company,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "salary_type": salary_type,
                "city": city,
            }
        next_page = response.css(
            "div.lg\\:container a.flex.rounded-full.text-base::attr(href)"
        ).get()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # /html/body/section/main/div[1]/div/ul/li[10]/a
        # /html/body/section/main/div[1]/div/ul/li[10]/a
        # or +25

        next_page_url = urljoin(url_general, next_page)
        print(next_page_url)
        if next_page:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_link,
                meta={"general_url": url_general},
            )

        # yield {"name": name, "url": url, "category_id": category_id}


# scrapy crawl cv_market_links_spider -o output.json
#
