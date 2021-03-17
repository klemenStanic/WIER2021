import time
from config import Config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class PageHandler:
    page_url = None

    def __init__(self, url):
        self.page_url = url
        self.scrape_the_page()


    def scrape_the_page(self):
        firefox_options = FirefoxOptions()

        # Adding a specific user agent
        firefox_options.add_argument("user-agent=fri-ieps-kslk")
        firefox_options.add_argument("--headless")

        print(f"Retrieving web page URL '{self.page_url}'")
        driver = webdriver.Firefox(options=firefox_options, executable_path=Config.WEB_DRIVER_LOCATION_GECKO)

        driver.get(self.page_url)

        # Timeout needed for Web page to render (read more about it)
        time.sleep(Config.RENDERING_TIMEOUT)

        html_content = driver.page_source
        base_url = self.get_base_url(driver)
        print(self.get_links(driver, base_url))
        driver.close()

    @staticmethod
    def get_links(driver, base_url):
        links = []
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href.startswith("/"):
               links.append(base_url + href)
            elif href is not None and ("http" in href or "https" in href):
                links.append(href)
        return links

    @staticmethod
    def get_base_url(driver):
        return driver.find_elements_by_tag_name('base')[0].get_attribute("href")

ph = PageHandler("http://evem.gov.si")
