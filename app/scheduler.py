import datetime
import socket
from models import *

class Scheduler:
    def __init__(self, seed=False, seed_path=None):
        self.session = Session(engine)
        if seed:
            self.load_seed(seed_path)
    
    def update_schedule(self, site_id, site_ip, timestamp):
        schedule = Schedule()
        schedule.site_id = site_id
        schedule.site_ip = site_ip
        schedule.timestamp = timestamp
        self.session.add(schedule)
        self.session.commit()
        return self.session.query(Schedule).filter(Schedule.site_id == site_id).first()

    def insert_site(self, domain):
        site = Site()
        site.domain = domain
        self.session.add(site)
        self.session.commit()
        return self.session.query(Site).filter(Site.domain==domain).first()

    def get_ip(self, domain):
        return  socket.gethostbyname(domain)

    def load_seed(self, seed_path):
        with open(seed_path) as seed_file:
            for domain in seed_file:
                domain = domain.strip()
                ip = self.get_ip(domain)
                site = self.insert_site(domain)
                self.update_schedule(site.id, ip, 0)

    def get_free_site(self):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        timestamp = current_time.timestamp() - 5
        site_result = self.session.query(Schedule).filter(Schedule.timestamp <= int(timestamp)).first()
        if site_result is not None:
            return site_result.site_id
        return None

    def update_schedule(self, site_id):
        schedule = self.session.query(Schedule).filter(Schedule.site_id==site_id).first()
        schedule.timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.session.commit()