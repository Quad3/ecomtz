import undetected_chromedriver as uc

from .main import Parser, get_soup, to_digit


class WBParser(Parser):
    def parse_page(self, browser: uc.Chrome, url: str) -> list[dict[str, str]]:
        soup = get_soup(browser, url, 30)
        try:
            body = soup.find("body")
            products_container = body.find("div", attrs={"class": "product-card-list"})
            if not products_container:
                print("WB blocked")
                return []

            products = products_container.find_all("article", recursive=False)

            res = []
            for product in products:
                product = product.find("div")
                link = product.find("a")
                product_info = product.find("div", attrs={"class": "product-card__middle-wrap"}, recursive=False)
                prices_div = product_info.find("span", attrs={"class": "price__wrap"})
                if not prices_div:
                    sale_price = ""
                    full_price = ""
                else:
                    sale_price = prices_div.find("ins")
                    full_price = prices_div.find("del")
                if bool(full_price and sale_price):
                    full_price = to_digit(full_price.text)
                    sale_price = to_digit(sale_price.text)
                else:
                    full_price = to_digit(sale_price.text)
                    sale_price = full_price
                product_data = {
                    "title": link["aria-label"],
                    "sale_price": round(float(sale_price), 2),
                    "full_price": round(float(full_price), 2),
                    "link": link["href"],
                }
                res.append(product_data)

            return res
        except Exception:
            print("WB error")
