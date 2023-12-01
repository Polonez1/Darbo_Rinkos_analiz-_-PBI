from playwright.sync_api import Playwright, sync_playwright, expect


class CVonlineParse:
    general_url: str = "https://www.cvonline.lt"

    def __init__(self):
        self.category_hrefs: dict = {}

    def __collect_hrefs(self):
        category_block = self.page.wait_for_selector(".categories__vacancy_categories")
        if category_block:
            links = category_block.query_selector_all("a")
            for link in links:
                href = link.get_attribute("href")
                name = link.inner_text()
                self.category_hrefs[name] = href

    def __parse_links(self):
        for key in self.category_hrefs.keys():
            name = key
            href = self.category_hrefs[key]

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.cvonline.lt/lt/categories")
            self.page.locator(".jsx-4189752321").first.click()
            self.page.get_by_label("Accept cookies").click()
            self.__collect_hrefs()
            self.__parse_links()


if "__main__" == __name__:
    cv = CVonlineParse()
    cv.parse()
