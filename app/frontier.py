from models import *

class Frontier:
    def __init__(self):
        self.session = Session(engine)

    def get_next_url(self):
        result = self.session.query(Page).filter(Page.accessed_time == None).order_by(Page.id.asc()).first()
        # TODO update db with new timestamp at Page.accessed_time
        return result


# for testing
if __name__ == '__main__':
    frontier = Frontier()
    print(frontier.get_next_url())