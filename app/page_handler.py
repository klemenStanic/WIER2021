import time
from models import *
from config import Config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helpers import *

from psycopg2.errors import *
from sqlalchemy.exc import *

from urllib.parse import urlparse
import requests
import hashlib

import urlcanon

class PageHandler:
    session = None
    driver = None

    page_db = None
    page_id = None
    page_url = None

    site_db = None
    site_id = None
    site_url = None

    content_type = None
    hashed_content = None
    html_content = None
    status_code = None

    def __init__(self, page_id):
        # Initialize variables
        self.session = Session(engine)

        self.page_id = page_id
        self.page_db = self.session.query(Page).filter(Page.id == self.page_id).first()
        self.page_url = self.page_db.url

        self.site_id = self.page_db.site_id
        self.site_db = self.session.query(Site).filter(Site.id == self.site_id).first()
        self.site_url = self.site_db.domain
        #self.preprocess()
        #self.main()
        
    def preprocess(self):
        # Lock the page that we are currently working on by setting page_type_code to None --------
        self.page_db.page_type_code = None
        self.session.commit()

        # Check whether the page is HTML, otherwise save as binary and terminate ------------------
        # Sometimes, there is a problem when establishing the ssl connection (Insecure connection),
        # so we catch the exception
        try:
            req = requests.get(self.page_url)
            content_type = req.headers["Content-Type"]
            self.content_type = content_type
            self.status_code = req.status_code
        except Exception:
            self.page_db.http_status_code = 443
            self.page_db.page_type_code = "ERROR"
            self.page_db.accessed_time = getTimestamp()
            self.session.commit()
            self.session.close()
            raise

        if "text/html" not in content_type:
            print(f"[PageHandler] Page {self.page_url} is not a html site.")
            type_of_content = get_type_of_content(content_type)
            if type_of_content:
                page_data = PageData()
                page_data.page_id = self.page_id
                page_data.data_type_code = type_of_content
                self.session.add(page_data)
                self.session.commit()
            self.page_db.page_type_code = "BINARY"
            self.page_db.http_status_code = self.status_code
            self.page_db.site_id = self.site_id
            self.page_db.url = self.page_url
            self.page_db.accessed_time = getTimestamp()
            self.session.commit()
            self.session.close()
            #self.driver.close()
            return False
        return True

    def main(self):        
        # The page contains HTML, lets scrape it --------------------------------------------------
        firefox_options = FirefoxOptions()

        # Adding a specific user agent
        firefox_options.add_argument("user-agent=fri-ieps-kslk")
        firefox_options.add_argument("--headless")

        print(f"[PageHandler] Retrieving web page URL '{self.page_url}'")
        self.driver = webdriver.Firefox(options=firefox_options, executable_path=Config.WEB_DRIVER_LOCATION_GECKO)

        self.driver.get(self.page_url)

        # Timeout needed for Web page to render (read more about it)
        time.sleep(Config.RENDERING_TIMEOUT)

        self.html_content = self.driver.page_source

        # Checking for duplicates ------------------------------------------------------------------
        self.hashed_content = hashlib.md5(self.html_content.encode("utf-8")).hexdigest()


        is_duplicate = self.session.query(Page).filter(Page.content_hash == self.hashed_content).first()
        if is_duplicate:
            self.page_db.page_type_code = "DUPLICATE"
            self.page_db.http_status_code = self.status_code
            self.page_db.site_id = self.site_id
            self.page_db.url = self.page_url
            self.page_db.accessed_time = getTimestamp()
            self.page_db.content_hash = self.hashed_content
            self.session.commit()
            self.session.close()
            self.driver.close()
            return

        # The page is valid html and its not a duplicate, now we extract all the links on the page ---
        links = []

        # First, we extract the links with tag name "a"
        # TODO: this section could use some work
        elems = self.driver.find_elements_by_tag_name("a")
        for elem in elems:
            href = elem.get_attribute('href')
            if href is None:
                continue
            if href.startswith("/"):
               links.append(self.base_url + href)
            elif href is not None and ("http" in href or "https" in href):
                links.append(href)

        # We also extract links from the onclick sections
        onclicks = self.driver.find_elements_by_xpath("//*[@onclick]")
        for el in onclicks:
            temp = el.get_attribute("onclick")
            if "location.href=" in temp:
                temp = temp.replace("location.href=", "")\
                    .replace("\'", "")\
                    .replace("\"", "")
                links.append(temp)

        # Remove the links that point outside of .gov
        links_trancuted = []
        for el in links:
            if "gov.si/" in el:
                links_trancuted.append(el)

        links = links_trancuted

        # Put the links in the canonical form
        links_canonical = []
        for el in links:
            parsed_link = urlcanon.parse_url(el)
            urlcanon.whatwg(parsed_link)
            links_canonical.append(str(parsed_link))

        links = links_canonical

        # Save the links to the DB -----------------------------------------------------------------
        for link in links:
            # Check if link is already in the DB
            is_duplicate = self.session.query(Page).filter(Page.url == link).first()
            if is_duplicate is None:
                extracted_domain_name = get_domain_name_from_url(link)

                page = Page()
                page.site_id = self.get_site_id_for_page(extracted_domain_name)

                # Pages with status == None have yet to be visited
                page.status = None
                page.page_type_code = "FRONTIER"
                page.url = link
                self.session.add(page)
                self.session.commit()

                # Also add a Link to the DB
                link_ = Link()
                link_.from_page = self.page_id
                link_.to_page = self.session.query(Page).filter(Page.url == link).first().id
                self.session.add(link_)
                self.session.commit()
            #else:
            #    print(f"Page {link} is already in the DB")

        # Finding and storing the images on the page --------------------------------------------------
        imgs = self.driver.find_elements_by_tag_name("img")
        for elem in imgs:
            src = elem.get_attribute("src")
            url = ""
            if src is None:
                continue
            if src.startswith("/"):
                url = self.base_url + src
            elif src is not None and ("http" in src or "https" in src):
                url = src
            if url != "" and len(url) <= 255:
                # Save the image
                image = Image()
                image.page_id = self.page_id
                image.filename = url
                image.content_type = "BINARY"
                image.accessed_time = getTimestamp()
                self.session.add(image)
                self.session.commit()

        # With all the data scraped, we can save the page to the DB -------------------------------------
        self.page_db.html_content = self.html_content
        self.page_db.accessed_time = getTimestamp()
        self.page_db.content_hash = self.hashed_content
        self.page_db.http_status_code = self.status_code
        self.page_db.site_id = self.site_id
        self.page_db.page_type_code = "HTML"
        self.page_db.url = self.page_url
        self.session.commit()

        # Lets be responsible and close the session and the driver
        self.session.close()
        self.driver.close()

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


def get_type_of_content(content_type):
    types = {
        "application/pdf":                                                           "PDF",
        "application/msword":                                                        "DOC",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":   "DOCX",
        "application/vnd.ms-powerpoint":                                             "PPT",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX"
    }

    if content_type in types:
        return types[content_type]
    return None



def get_domain_name_from_url(url):
    domain = urlparse(url).netloc
    return domain






