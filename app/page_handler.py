import time
from models import *
from config import Config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helpers import *

from urllib.parse import urlparse
import requests
import hashlib





class PageHandler:
    page_url = None
    base_url = None
    page_id = None
    site_id = None

    session = None

    driver = None

    links = None
    images = None
    html_content = None
    status_code = None

    def __init__(self, page_id):
        self.page_id = page_id
        self.session = Session(engine)
        self.page_url = self.get_page_url_and_lock_the_page()
        self.site_id = self.get_site_id()
        self.base_url = self.get_base_url()

        # Check if the page is html, otherwise save as binary and terminate
        req = requests.get(self.page_url)
        content_type = requests.head(self.page_url).headers["Content-Type"]
        self.status_code = req.status_code
        if content_type != "text/html":
            current_page = self.session.query(Page).filter(Page.id == self.page_id).first()
            current_page.page_type_code = "BINARY"
            current_page.status_code = self.status_code
            current_page.site_id = self.site_id
            current_page.url = self.page_url
            current_page.accessed_time = getTimestamp()
            return

        # Check for duplicates

        self.scrape_the_page()

        self.finalize_page()


    def get_page_url_and_lock_the_page(self):
        current_page = self.session.query(Page).filter(Page.id == self.page_id).first()
        page_url = current_page.url
        current_page.page_type_code = None
        self.session.commit()
        return page_url


    def finalize_page(self):
        current_page = self.session.query(Page).filter(Page.id == self.page_id).first()
        current_page.html_content = self.html_content
        current_page.accessed_time = getTimestamp()
        current_page.status_code = self.status_code


    def get_site_id(self):
        result = self.session.query(Page).filter(Page.id == self.page_id).first().site_id
        return result

    def get_base_url(self):
        result = self.session.query(Site).filter(Site.id == self.site_id).first().domain
        return result

    def scrape_the_page(self):
        firefox_options = FirefoxOptions()

        # Adding a specific user agent
        firefox_options.add_argument("user-agent=fri-ieps-kslk")
        firefox_options.add_argument("--headless")

        print(f"Retrieving web page URL '{self.page_url}'")
        self.driver = webdriver.Firefox(options=firefox_options, executable_path=Config.WEB_DRIVER_LOCATION_GECKO)

        self.driver.get(self.page_url)

        # Timeout needed for Web page to render (read more about it)
        time.sleep(Config.RENDERING_TIMEOUT)

        self.html_content = driver.page_source

        # Check for duplicates
        hashed_content = hashlib.md5(self.html_content).hexdigest()

        result = self.session.query(Page).filter(Page.content_hash == hashed_content).first()
        if result:
            current_page = self.session.query(Page).filter(Page.id == self.page_id).first()
            current_page.page_type_code = "DUPLICATE"
            current_page.status_code = self.status_code
            current_page.site_id = self.site_id
            current_page.url = self.page_url
            current_page.accessed_time = getTimestamp()
            return

        # Uncomment ˇ to use the <base> in the page, might not be present in all pages
        # self.base_url = self.get_base_url()

        self.links = self.get_links()

        self.images = self.get_images()
        self.driver.close()



    def save_pages_to_db(self):
        for link in self.links:
            page = Page()
            page.site_id = self.get_site_id_for_page(self.get_domain_name_from_url(link))
            # If page has status of none, the page has not yet been visited
            page.status = None
            page.page_type_code = "FRONTIER"
            page.url = link
            self.session.add(page)
            self.session.commit()

            link_ = Link()
            link_.from_page = self.page_id
            link_.to_page = self.session.query(Page).filter(Page.url == link).first().id
            self.session.add(link_)
            self.session.commit()


    def get_domain_name_from_url(self, url):
        domain = urlparse(url).netloc
        return domain


    def get_site_id_for_page(self, url):
        """
        Checks the db whether a site with the same domain exists. If not, it creates a new site
        and return the site's id.
        :param url:
        :return: site_id
        """
        result = self.session.query(Site).filter(Site.domain == url).first()
        if result:
            return result.id
        site = Site()
        site.domain = url
        self.session.add(site)
        self.session.commit()
        return self.session.query(Site).filter(Site.domain == url).first().id


    def save_images_to_db(self):
        for i in self.images:
            image = Image()
            image.page_id = self.page_id
            image.filename = i
            image.content_type = "BINARY"
            image.accessed_time = getTimestamp()
            self.session.add(image)
            self.session.commit()


    def remove_non_gov_sites(self, sites):
        out = []
        for el in sites:
            if "gov.si" in el:
                out.append(el)
        return out


    def get_images(self):
        out = []
        imgs = self.driver.find_elements_by_tag_name("img")
        for elem in imgs:
            src = elem.get_attribute("src")
            if src.startswith("/"):
                out.append(self.base_url + src)
            elif src is not None and ("http" in src or "https" in src):
                out.append(src)
        return out


    def get_links(self):
        links = []
        elems = self.driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href.startswith("/"):
               links.append(self.base_url + href)
            elif href is not None and ("http" in href or "https" in href):
                links.append(href)

        onclicks = self.driver.find_elements_by_xpath("//*[@onclick]")

        # TODO: base_url check
        for el in onclicks:
            temp = el.get_attribute("onclick")
            if "location.href=" in temp:
                temp = temp.replace("location.href=", "")\
                    .replace("\'", "")\
                    .replace("\"", "")
                links.append(temp)

        return self.remove_non_gov_sites(links)

"""
    def get_base_url(self):
        bases = self.driver.find_elements_by_tag_name('base')
        if len(bases) > 0:
            return bases[0].get_attribute("href")
        return None
"""
#ph = PageHandler("http://evem.gov.si")
#ph = PageHandler("https://www.w3schools.com/jsref/event_onclick.asp")
