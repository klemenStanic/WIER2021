from crawler import Crawler
from page_handler import PageHandler
from config import Config

from selenium.common.exceptions import  InvalidSessionIdException

import concurrent.futures
import threading
import time
import copy
import sys
import traceback

from models import *

lock = threading.Lock()

# config options
SEED = Config.SEED
SEED_PATH = Config.SEED_PATH
WORKERS = Config.WORKERS
LOG_PATH = Config.LOG_PATH

def run_page_handlers(page_id):
    print(f"[Main] Crawling page with id: {page_id}")
    page_handler = None
    try:
        page_handler = PageHandler(page_id)
        flag = page_handler.preprocess()
        if flag:
            page_handler.main()
    except Exception as e:
        # Lets close the driver
        try:
            page_handler.driver.close()
        except Exception:
            print("[Main] Tried to close the driver after an error, but the driver is already closed.")

        print(f"[Main] Error at page: {page_id}")
        # Write log file
        with open(f'{LOG_PATH}/page_{page_id}.log','w') as file:
            file.write(str(e))
            file.write(traceback.format_exc())
        # Mark it in DB
        session = Session(engine)
        page = session.query(Page).filter(Page.id==page_id).first()
        page.page_type_code = 'ERROR'
        session.commit()
        session.close()
    print(f"[Main] Finished crawling page with id: {page_id}")
    sys.stdout.flush()
    return


crawler = Crawler(seed=SEED, seed_path=SEED_PATH)
print(f"[Main] Starting Crawler {'with' if SEED else 'without'} Seed\n ... executing {WORKERS} workers ...\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    while True:
        page_id = crawler.frontier.get_next_url()
        if page_id is None:
            sys.stdout.flush()
            time.sleep(1)
            continue
        executor.submit(run_page_handlers, copy.deepcopy(page_id))