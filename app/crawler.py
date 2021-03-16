from frontier import Frontier


class Crawler:
    def __init__(self, num_of_workers=1):
        self.n_workers = num_of_workers
        self.frontier = Frontier()
        

    def init_db_connections(self):
        """
        Initializes the connection to the db, and creates the corresponding objects.
        :return:
        """
        pass

    
