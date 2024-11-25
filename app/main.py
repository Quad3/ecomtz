import random
import time
from datetime import datetime
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import Future

from parser.main import init_webdriver, Parser
from parser.ozon import OzonParser
from parser.auchan import AuchanParser
from parser.wb import WBParser
from database import save_data


def parse_and_save(parsers: list[Parser], workers: int) -> None:
    futures: list[Future] = []
    browser_count: int = workers
    browsers = [init_webdriver() for _ in range(browser_count)]

    tasks = []
    for parser in parsers:
        for url in parser.urls:
            tasks.append((parser, url))
    random.shuffle(tasks) # parse urls in random order

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (parser, url) in enumerate(tasks):
            futures.append(ex.submit(parser.parse_page, browsers[i % browser_count], url))
            time.sleep(round(random.random(), 1)) # to avoid bot detection

    for future in futures:
        res = future.result()
        save_data(res)


def main():
    ozon_urls = [
        "https://www.ozon.ru/category/elektronika-15500/",
        "https://www.ozon.ru/category/dom-i-sad-14500/",
        "https://www.ozon.ru/category/detskie-tovary-7000/",
    ]
    wb_urls = [
        "https://www.wildberries.ru/catalog/novyy-god/simvol-goda",
        "https://www.wildberries.ru/catalog/tsvety",
        "https://www.wildberries.ru/catalog/sport/vidy-sporta/velosport/velosipedy",
    ]
    auchan_urls = [
        "https://www.auchan.ru/catalog/novyy-god/novogodnie-dekoracii/elektrogirlyandy-i-svetovoy-dekor/",
        "https://www.auchan.ru/catalog/novyy-god/",
        "https://www.auchan.ru/catalog/novyy-god/podarki/",
    ]

    print("Start parsing")
    start = datetime.now()

    ozon = OzonParser(ozon_urls, 1)
    wb = WBParser(wb_urls, 3)
    auchan = AuchanParser(auchan_urls, 3)

    parsers = [ozon, wb, auchan]
    parse_and_save(parsers, workers=1)

    print(datetime.now() - start)


if __name__ == "__main__":
    main()
