import time
from models import *
from config import Config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helpers import *

class PageHandler:
    page_url = None
    page_id = None
    session = None

    def __init__(self, url):
        self.page_url = url
        self.page_id = self.get_page_id()
        self.session = Session(engine)
        self.scrape_the_page()


    def get_page_id(self):
        result = self.session.query(Page).filter(Page.url == self.page_url).first()
        return result


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

        links = self.get_links(driver, base_url)

        images = self.get_images(driver, base_url)
        driver.close()


    def save_pages_to_db(self, links):
        id = Column('id', Integer, primary_key=True)
        site_id = Column('site_id', Integer, ForeignKey(Site.id))
        status = Column('status', Boolean)
        page_type_code = Column('page_type_code', String, ForeignKey(PageType.code))
        url = Column('url', String)
        html_content = Column('html_content', Text)
        html_status_code = Column('http_status_code', Integer)
        accessed_time = Column('accessed_time', BigInteger)

        for link in links:
            page = Page()
            page.site_id =



    def save_images_to_db(self, images):
        for i in images:
            image = Image()
            image.page_id = self.page_id
            image.filename = i
            image.content_type = "BINARY"
            image.accessed_time = getTimestamp()
            self.session.add(image)
            self.session.commit()


    @staticmethod
    def remove_non_gov_sites(sites):
        out = []
        for el in sites:
            if "gov.si" in el:
                out.append(el)
        return out


    @staticmethod
    def get_images(driver, base_url):
        out = []
        imgs = driver.find_elements_by_tag_name("img")
        for elem in imgs:
            src = elem.get_attribute("src")
            if src.startswith("/"):
                out.append(base_url + src)
            elif src is not None and ("http" in src or "https" in src):
                out.append(src)
        return out


    def get_links(self, driver, base_url):
        links = []
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href.startswith("/"):
               links.append(base_url + href)
            elif href is not None and ("http" in href or "https" in href):
                links.append(href)

        onclicks = driver.find_elements_by_xpath("//*[@onclick]")

        # TODO: base_url check
        for el in onclicks:
            temp = el.get_attribute("onclick")
            if "location.href=" in temp:
                temp = temp.replace("location.href=", "")\
                    .replace("\'", "")\
                    .replace("\"", "")
                links.append(temp)

        return self.remove_non_gov_sites(links)


    @staticmethod
    def get_base_url(driver):
        bases = driver.find_elements_by_tag_name('base')
        if len(bases) > 0:
            return bases[0].get_attribute("href")
        return None

#ph = PageHandler("http://evem.gov.si")
#ph = PageHandler("https://www.w3schools.com/jsref/event_onclick.asp")
