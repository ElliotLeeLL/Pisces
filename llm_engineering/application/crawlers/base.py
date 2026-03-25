from abc import ABC, abstractmethod
import time
import os
from tempfile import mkdtemp
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from llm_engineering.domain.base import NoSQLBaseDocument

# # Install or load chromedriver
# chromedriver_path = "/usr/local/bin/chromedriver"

# if os.path.exists(chromedriver_path):
#     print(f"The file '{chromedriver_path}' exists.")
# else:
#     print(f"The file '{chromedriver_path}' does not exist.")
# # chromedriver_autoinstaller.install(path=chromedriver_path)


class BaseCrawler(ABC):
    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...

class BaseSeleniumCrawler(BaseCrawler, ABC):
    def __init__(self, scroll_limit: int = 5) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9226")

        self.set_extra_driver_options(options)

        self.scroll_limit = scroll_limit

        chromedriver_path = "/usr/local/bin/chromedriver"
        try:
            # Try to load the local ChromeDriver
            if not os.path.exists(chromedriver_path):
                raise FileNotFoundError("Local ChromeDriver not found.")
            driver = webdriver.Chrome(
                options=options,
                executable_path=chromedriver_path,
            )
            print("ChromeDriver loaded from the local file.")

        except (FileNotFoundError, Exception) as e:
            # If there's an error, install ChromeDriver automatically
            print(f"Error: {e}. Installing ChromeDriver.")
            chromedriver_autoinstaller.install()
            self.driver = webdriver.Chrome(
                options=options,
            )
    
    def set_extra_driver_options(self, options: Options) -> None:
        pass
    
    def login(self) -> None:
        pass

    def scroll_page(self) -> None:
        current_scroll = 0
        last_height = self.driver.excute_script("return document.body.scrollHeight")
        while True:
            self.driver.excute_script("Window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or (self.scroll_limit and current_scroll >= self.scroll_limit):
                break
            last_height = new_height
            current_scroll += 1