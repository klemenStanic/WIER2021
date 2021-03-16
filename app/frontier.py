from models import *
from scheduler import Scheduler

class Frontier:
    def __init__(self):
        self.session = Session(engine)
        self.scheduler = Scheduler()

    def get_next_url(self):
        # TODO check scheduler first
        result_page = self.session.query(Page).filter(Page.accessed_time == None).order_by(Page.id.asc()).first()
        if result_page is None:
            return None
        result_site = self.session.query(Site).filter(Site.id == result_page.site_id).first()
        # TODO update db with new timestamp at Page.accessed_time
        return result_site.domain + result_page.url




# for testing
if __name__ == '__main__':
    frontier = Frontier()
    print(frontier.get_next_url())