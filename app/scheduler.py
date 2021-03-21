import datetime
import socket
from models import *

class Scheduler:
    def __init__(self, seed=False, seed_path=None):
        self.session = Session(engine)
        if seed:
            self.load_seed(seed_path)
    
    def insert_site(self, domain, ip):
        site = Site()
        site.domain = domain
        site.site_ip = ip
        site.timestamp = 0
        self.session.add(site)
        self.session.commit()
        return self.session.query(Site).filter(Site.domain==domain).first()

    def get_ip(self, domain):
        ip = None
        try:
            ip = socket.gethostbyname(domain)
        except:
            ip = None
        return ip

    def load_seed(self, seed_path):
        with open(seed_path) as seed_file:
            for domain in seed_file:
                domain = domain.strip()
                ip = self.get_ip(domain)
                site = self.insert_site(domain, ip)

    def update_sites(self):
        sites = self.session.query(Site).filter(Site.site_ip==None).all()
        for site in sites:
            site.site_ip = self.get_ip(site.domain)
            site.timestamp = 0
        self.session.commit()

    def update_timestamp(self, site_id):
        site_result = self.session.query(Site).filter(Site.id==site_id).first()
        site_result.timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        self.session.commit()

    def get_free_site(self):
        self.update_sites()
        current_time = datetime.datetime.now(datetime.timezone.utc)
        timestamp = current_time.timestamp() - 5
        site_result = self.session.query(Site).filter(Site.done==None).filter(Site.timestamp <= int(timestamp)).filter(Site.site_ip!=None).first()
        if site_result is not None:
            return site_result.id
        return None

    def remove_site(self, site_id):
        site = self.session.query(Site).filter(Site.id == site_id).first()
        site.done = True
        self.session.commit()
        print(f'[Scheduler] Site {site_id} finished!')
