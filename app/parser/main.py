import time
import random
from abc import abstractmethod

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from undetected_chromedriver.options import ChromeOptions
from selenium_stealth import stealth


def init_webdriver():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled") # prevents blocking
    # options.add_argument("--blink-settings=imagesEnabled=false") # dont load pictures
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    options.add_argument(f"--user-agent={custom_user_agent}")

    driver = uc.Chrome(
        options=options,
        version_main=131,
        use_subprocess=False,
        driver_executable_path="/usr/bin/chromedriver",
    )
    stealth(
        driver,
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


def to_digit(s: str) -> str:
    return ''.join(e for e in s if e in "1234567890,.").replace(',', '.')


def scrolldown(browser: uc.Chrome, deep):
    for _ in range(deep):
        browser.execute_script('window.scrollBy(0, 500)')
        time.sleep(round(0.1 * random.random(), 1))


def get_soup(browser: uc.Chrome, url: str, scroll: int):
    browser.get(url)
    time.sleep(6.5) # wait for page load
    scrolldown(browser, scroll)
    time.sleep(4.5)

    return BeautifulSoup(browser.page_source, "html.parser")


class Parser:
    def __init__(self, urls: list[str], page_number: int):
        self.urls = []
        for url in urls:
            for page in range(1, page_number + 1):
                if page != 1:
                    new_url = url + f"?page={page}"
                else:
                    new_url = url
                self.urls.append(new_url)

        self.page_number = page_number

    @abstractmethod
    def parse_page(self, browser: uc.Chrome, url: str):
        raise NotImplemented
