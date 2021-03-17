from crawler import Crawler

# config options
SEED = False
SEED_PATH = 'seed.txt'


crawler = Crawler(seed=SEED, seed_path=SEED_PATH)
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
print(crawler.frontier.get_next_url())
