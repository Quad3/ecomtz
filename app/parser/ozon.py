import undetected_chromedriver as uc

from .main import Parser, get_soup, to_digit


class OzonParser(Parser):
    def __init__(self, urls: list[str], page_number: int):
        super().__init__(urls, page_number)
        self.host = "https://www.ozon.ru"

    def parse_page(self, browser: uc.Chrome, url: str) -> list[dict[str, str]]:
        soup = get_soup(browser, url, 50)

        body = soup.find("body")
        products_container = body.find("div", {"id": "paginatorContent"})
        if not products_container:
            print("Ozon blocked")
            return []

        res = []
        for inner_container in products_container.find_all("div", recursive=False):
            try:
                products = inner_container.find("div").find_all("div", recursive=False)
                for product in products:
                    product_info = product.find("div").find("div", recursive=False).find_all("div", recursive=False)
                    prices_div = product_info[0].find("div")
                    if not prices_div:
                        continue

                    prices = prices_div.find_all("span")[:2]
                    link = product.find("a")
                    link = self.host + link["href"][:link["href"].find('?')]
                    sale_price = round(float(to_digit(prices[0].text)), 2)
                    full_price = to_digit(prices[1].text)
                    if full_price:
                        full_price = round((float(full_price)), 2)
                    else:
                        full_price = sale_price

                    count = product_info[1].find("span", attrs={"class": "tsBody400Small"})
                    if count:
                        count = to_digit(count.text)
                        if count != "":
                            count = int(count)
                        else:
                            count = None
                    title = product.find("div").find("div", recursive=False).find("a", recursive=False).find("span").text

                    product_data = {
                        "title": title,
                        "sale_price": sale_price,
                        "full_price": full_price,
                        "link": link,
                        "count": count,
                    }
                    res.append(product_data)
            except Exception:
                print("Ozon error")

        return res
