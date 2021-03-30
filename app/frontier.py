from models import *
from scheduler import Scheduler
import requests
from reppy.robots import Robots

class Frontier:
    def __init__(self, seed=False, seed_path=None):
        self.session = Session(engine)
        self.scheduler = Scheduler(seed=seed, seed_path=seed_path)

    def get_sitemap(self, site_id, sitemap_url):
        result_site = self.session.query(Site).filter(Site.id == site_id).first()
        if result_site.sitemap_content is None:
            try:
                resp = requests.get(sitemap_url)
                result_site.sitemap_content = resp.text
            except Exception:
                result_site.sitemap_content = "Not found"
            self.session.commit()

    def parse_robots(self, robots_text):
        robots_json = {
            'disallow': [],
            'allow': [],
            'sitemap': None
        }
        if '404' in robots_text:
            return robots_json

        return robots_json

    def get_site_robots(self, site_id):
        if site_id is None:
            return None
        result_site = self.session.query(Site).filter(Site.id == site_id).first()
        if result_site.robots_content is None:
            try:
                resp = requests.get(f'http://{result_site.domain}/robots.txt', timeout=3)
                result_site.robots_content = resp.text
                self.session.commit()
            except Exception:
                return self.parse_robots('404')
        return self.parse_robots(result_site.robots_content)

    def check_robots(self, page_id):
        result_page = self.session.query(Page).filter(Page.id==page_id).first()
        result_site = self.session.query(Site).filter(Site.id==result_page.site_id).first()
        try:
            robots = Robots.fetch(f'http://{result_site.domain}/robots.txt', timeout=3)
        except Exception:
            return True
        return robots.allowed(result_page.url, 'fri-ieps-kslk')

    def add_root_page(self, site_id):
        site = self.session.query(Site).filter(Site.id==site_id).first()
        # first check if page already exists
        root_page = self.session.query(Page).filter(Page.url==f'http://{site.domain}/').first()
        if root_page is not None:
            return root_page

        root_page = Page()
        root_page.site_id = site_id
        root_page.url = f'http://{site.domain}/'
        root_page.status = None
        root_page.page_type_code = 'FRONTIER' 
        self.session.add(root_page)
        self.session.commit()
        new_page = self.session.query(Page).filter(Page.url==f'http://{site.domain}/').first()
        return new_page

    def get_next_url(self):
        """
        This method checks if there is site/IP which hasn't been visited in last 5 seconds
        If it gets such site, it checks if there are any unvisited pages of this site and returns url.
        """
        site_id = self.scheduler.get_free_site()
        if site_id is None:
            return None
        print(f"[Frontier] Free site's id: {site_id}")
        robots_json = self.get_site_robots(site_id)
        if robots_json['sitemap'] is not None:
            self.get_sitemap(site_id, robots_json['sitemap'])
        #result_site = self.session.query(Site).filter(Site.id == site_id).first()
        result_page = self.session.query(Page).filter(Page.site_id == site_id).filter(Page.page_type_code == 'FRONTIER').order_by(Page.id.asc()).first()
        all_pages_count = self.session.query(Page).filter(Page.site_id == site_id).count()
        if result_page is None and all_pages_count == 0:  # we check if we need to add root page
            result_page = self.add_root_page(site_id)
        elif result_page is None and all_pages_count != 0:
            self.scheduler.remove_site(site_id)
            return self.get_next_url()  # apperently this site has been crawled and we can check for a new one
        # handle if crawler is even allowed on url
        if not self.check_robots(result_page.id):
            print(f'[Frontier] Not allowed on page {result_page.id}')
            result_page.page_type_code = 'DISALLOWED'
            self.session.commit()
            return self.get_next_url()
        result_page.page_type_code = None  # we lock this page
        self.session.commit()
        self.scheduler.update_timestamp(site_id)  # update scheduler with new timestamp
        return result_page.id





# for testing
if __name__ == '__main__':
    frontier = Frontier()
    print(frontier.get_next_url())
