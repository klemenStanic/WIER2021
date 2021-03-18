from frontier import Frontier


class Crawler:
    def __init__(self, num_of_workers=1, seed=False, seed_path=None):
        self.n_workers = num_of_workers
        self.frontier = Frontier(seed=seed, seed_path=seed_path)

    
