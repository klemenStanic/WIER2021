from crawler import Crawler
from page_handler import PageHandler

# config options
SEED = False
SEED_PATH = 'seed.txt'


crawler = Crawler(seed=SEED, seed_path=SEED_PATH)
for i in range(10):
    page_id = crawler.frontier.get_next_url()
    print(f"Crawling page: {page_id}")
    page_handler = PageHandler(page_id)