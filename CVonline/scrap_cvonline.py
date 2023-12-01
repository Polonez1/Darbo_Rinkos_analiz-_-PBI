from playwright.sync_api import Playwright, sync_playwright, expect
import time
import json


class CVonlineParse:
    general_url: str = "https://www.cvonline.lt"

    def __init__(self):
        self.category_hrefs: dict = {}
        self.full_data: list = []

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

    def __output(self, data):
        output_file_path = "./output/cvonline.json"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(self.full_data, output_file, ensure_ascii=False, indent=2)

    def __collect_hrefs(self):
        category_block = self.page.wait_for_selector(".categories__vacancy_categories")
        if category_block:
            links = category_block.query_selector_all("a")
            for link in links:
                href = link.get_attribute("href")
                name = link.inner_text()
                self.category_hrefs[name] = href

    def __collect_vacancies(self, vacancies, url_general):
        page = 1
        while True:
            time.sleep(2)
            for vacancy in vacancies:
                url_general = url_general
                href = vacancy.query_selector(".vacancy-item").get_attribute("href")
                description = (
                    vacancy.query_selector(".vacancy-item__title").inner_text().strip()
                )
                company = (
                    vacancy.query_selector(".vacancy-item__column a")
                    .inner_text()
                    .strip()
                )
                try:
                    _salary = vacancy.eval_on_selector(
                        ".vacancy-item__salary-label", "(element) => element.innerText"
                    )
                except:
                    _salary = None
                salary_from = self.__salary_split(_salary, 0)
                salary_to = self.__salary_split(_salary, 2)

                _city = vacancy.query_selector(".vacancy-item__locations").inner_text()
                city = self.__city_split(_city)

                data = {
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
                self.full_data.append(data)
                print(page, description, salary_from, city)
                # print(page, company, _salary)

            next_button = self.page.query_selector("button[aria-label='Next']")
            page += 1
            if next_button:
                if next_button.is_enabled():
                    next_button.click()
                    time.sleep(10)
                    vacancies = self.page.query_selector_all(".vacancies-list__item")
                else:
                    break
            else:
                break

    def __parse_links(self):
        for key in self.category_hrefs.keys():
            name = key
            href = self.category_hrefs[key]
            url = self.general_url + href
            self.page.goto(url)
            vacancies = self.page.query_selector_all(".vacancies-list__item")
            self.__collect_vacancies(vacancies=vacancies, url_general=href)

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.cvonline.lt/lt/categories")
            self.page.locator(".jsx-4189752321").first.click()
            self.page.get_by_label("Accept cookies").click()
            self.__collect_hrefs()
            self.__parse_links()
            self.__output(data=self.full_data)


if "__main__" == __name__:
    cv = CVonlineParse()
    cv.parse()
    print(cv.full_data)
