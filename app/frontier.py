from models import *
from scheduler import Scheduler

class Frontier:
    def __init__(self, seed=False, seed_path=None):
        self.session = Session(engine)
        self.scheduler = Scheduler(seed=seed, seed_path=seed_path)

    def get_next_url(self):
        """
        This method checks if there is an site/IP which hasn't been visited in last 5 seconds
        If it gets such site, it checks if there are any unvisited pages of this site and returns url.
        """
        site_id = self.scheduler.get_free_site()
        result_site = self.session.query(Site).filter(Site.id == site_id).first()
        result_page = self.session.query(Page).filter(Page.site_id==site_id).filter(Page.accessed_time==None).order_by(Page.id.asc()).first()
        if result_site is None:
            return None
        self.scheduler.update_schedule(site_id) # update scheduler with new timestamp
        if result_page is None:
            return result_site.domain
        return result_site.domain + result_page.url




# for testing
if __name__ == '__main__':
    frontier = Frontier()
    print(frontier.get_next_url())