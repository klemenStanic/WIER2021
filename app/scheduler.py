import datetime

from models import *

class Scheduler:
    def __init__(self):
        self.session = Session(engine)
    
    def get_free_site(self):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        timestamp = current_time.timestamp() - 5
        site_result = self.session.query(Schedule).filter(Schedule.timestamp == int(timestamp)).first()
        return site_result