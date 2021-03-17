from models import *
from scheduler import Scheduler
import requests

class Frontier:
    def __init__(self, seed=False, seed_path=None):
        self.session = Session(engine)
        self.scheduler = Scheduler(seed=seed, seed_path=seed_path)

    def parse_robots(self, robots_text):
        robots_json = {
            'disallow': [],
            'allow': [],
            'sitemap': None
        }
        if '404' in robots_text:
            return robots_json

        for line in robots_text.replace('\r,' ,'').split('\n'):
            if "Disallow:" in line:
                robots_json['disallow'].append(line.split(' ')[1])
            elif "Allow:" in line:
                robots_json['allow'].append(line.split(' ')[1])
            elif "Sitemap:" in line:
                robots_json['sitemap']= line.split(' ')[1]
        return robots_json

    def get_site_robots(self, site_id):
        if site_id is None:
            return None
        result_site = self.session.query(Site).filter(Site.id == site_id).first()
        if result_site.robots_content is None:
            resp = requests.get(f'http://{result_site.domain}/robots.txt')
            result_site.robots_content = resp.text
            self.session.commit()
        return self.parse_robots(result_site.robots_content)

    def get_next_url(self):
        """
        This method checks if there is an site/IP which hasn't been visited in last 5 seconds
        If it gets such site, it checks if there are any unvisited pages of this site and returns url.
        """
        site_id = self.scheduler.get_free_site()
        robots_json = self.get_site_robots(site_id)
        result_site = self.session.query(Site).filter(Site.id == site_id).first()
        result_page = self.session.query(Page).filter(Page.site_id==site_id).filter(Page.accessed_time==None).order_by(Page.id.asc()).first()
        if result_site is None:
            return None
        self.scheduler.update_schedule(site_id) # update scheduler with new timestamp
        if result_page is None:
            return result_site.domain
        # handle if crawler is even allowed on url
        robots_json = self.get_site_robots(site_id)
        for disallow in robots_json['disallow']:
            # if crawler is not allowed on this url, update Page.accessed_time = -1 and call self function again 
            if disallow == result_page.url[:len(disallow)]:
                result_page.accessed_time = -1
                self.session.commit()
                return self.get_next_url()

        return result_site.domain + result_page.url




# for testing
if __name__ == '__main__':
    frontier = Frontier()
    print(frontier.get_next_url())