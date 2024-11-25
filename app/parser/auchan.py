import undetected_chromedriver as uc

from .main import Parser, get_soup, to_digit


class AuchanParser(Parser):
    def __init__(self, urls: list[str], page_number: int):
        super().__init__(urls, page_number)
        self.host = "https://www.auchan.ru"

    def parse_page(self, browser: uc.Chrome, url: str) -> list[dict[str, str]]:
        soup = get_soup(browser, url, 30)

        body = soup.find("body")
        body = body.find("div", attrs={"id": "root"}, recursive=False)
        if not body:
            print("Auchan blocked")
            return []

        body = body.find("div", attrs={"id": "container"}, recursive=False)
        body = body.find("div", attrs={"id": "main"}, recursive=False)
        body = body.find("main", recursive=False)
        body = body.find("div", recursive=False)
        body = body.find("div", recursive=False)
        body = body.find("div", recursive=False)
        body = body.find_all("div", recursive=False)[2]
        products_container = body.find("div", recursive=False)
        products = products_container.find_all("article")

        res = []
        for product in products:
            link = product.find("a", attrs={"class": "linkToPDP"}, recursive=False)
            title = link.find("p")
            prices_div = product.find("div", attrs={"class": "productCardPriceData"}, recursive=False)
            prices_div = prices_div.find_all("div", recursive=False)
            if len(prices_div) == 2:
                sale_price = to_digit(prices_div[0].text)
                full_price = to_digit(prices_div[1].text)
            else:
                full_price = to_digit(prices_div[0].text)
                sale_price = full_price

            product_data = {
                "link": self.host + link["href"],
                "title": title.text,
                "sale_price": round(float(sale_price), 2),
                "full_price": round(float(full_price), 2),
            }
            res.append(product_data)

        return res
