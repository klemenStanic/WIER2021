from crawler import Crawler
from page_handler import PageHandler
from config import Config

import concurrent.futures
import threading
import time
import copy
import sys

lock = threading.Lock()

# config options
SEED = Config.SEED
SEED_PATH = Config.SEED_PATH
WORKERS = Config.WORKERS
LOG_PATH = Config.LOG_PATH

def run_page_handlers(page_id):
    print(f"Crawling page: {page_id}")
    try:
        PageHandler(page_id)
    except Exception as e:
        print(f"Error at page: {page_id}")    
        with open(f'{LOG_PATH}/page_{page_id}.log','w') as file:
            file.write(str(e))
    return


crawler = Crawler(seed=SEED, seed_path=SEED_PATH)
print(f"Starting Crawler {'with' if SEED else 'without'} Seed\n ... executing {WORKERS} workers ...\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    while True:
        page_id = crawler.frontier.get_next_url()
        if page_id is None:
            sys.stdout.flush()
            time.sleep(1)
            continue
        executor.submit(run_page_handlers(copy.deepcopy(page_id)))