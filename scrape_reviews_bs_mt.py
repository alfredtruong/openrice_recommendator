#%%
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup  
import os
import queue
import random
import time

import threading

user_agents = [
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
]

#%%

def is_already_processed(file_path,url):
    with lock:
        try:
            with open(file_path, 'r') as f:
                if url in set(line.strip() for line in f):
                    print(f"[{url}] already processed, skipping...")
                    return True
                else:
                    print(f"[{url}] not processed, do now")
                    return False
        except FileNotFoundError:
            print(f"[{url}] not processed, do now")
            return False

def add_processed_url(file_path, url):
    with lock:
        with open(file_path, 'a') as f:
            f.write(url + '\n')

# Define a thread worker function
def worker(queue, user_agents):
    while True:
        # get url
        url = queue.get()
        if url is None:  # poison pill, exit the thread
            break

        if is_already_processed(PROCESSED_URLS,url):
            continue

        # standard sleep
        time.sleep(random.uniform(WAIT_MIN_SHORT, WAIT_MAX_SHORT))
        if random.random() < 0.2:
            time.sleep(random.uniform(WAIT_MIN_LONG, WAIT_MAX_LONG))

        # prep agent + get data
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)

        # extract reviews
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 'tab-pane content content-full js-content-full'})
        for review in reviews:
            # grab container
            review_container = review.find('section', {'class': 'review-container'})

            # remove 
            for element in review_container.find_all('a'):
                element.decompose()
            if review_container:
                yield {
                    'url': url,
                    'review': review_container.get_text(strip=True)
                }

        # Save the URL to the processed_urls file
        add_processed_url(PROCESSED_URLS, url)

def write_to_file(entry):
    with lock:
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            line = json.dumps(dict(entry), ensure_ascii=False) + "\n"
            f.write(line)

#%%

################################# SETTINGS
ALL_REVIEW_URLS_OUT = 'assets/all_review_urls.csv'
OUTPUT_FILE = 'assets/scrapes/output_bs.jsonl'
PROCESSED_URLS = 'assets/scrapes/output_bs_processed_urls.txt'
WORKERS = 10
MAX_URLS = 100
WAIT_MIN_SHORT, WAIT_MAX_SHORT = 1, 5
WAIT_MIN_LONG, WAIT_MAX_LONG = 30, 60

review_urls = pd.read_csv(ALL_REVIEW_URLS_OUT,header=None)[0].to_list()

################################# POPULATE QUEUE
# Create a queue to hold the URLs to be scraped
queue = queue.Queue()

# Add URLs to the queue
for url in review_urls[:MAX_URLS]:
    queue.put(url)

# Add poison pills to the queue to signal threads to exit
for _ in range(WORKERS):
    queue.put(None)

################################# POPULATE THREADS
# Create a list to hold the threads
lock = threading.Lock()
threads = []

# Create and start the threads
for i in range(WORKERS):
    t = threading.Thread(target=worker, args=(queue, user_agents))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()
#%%

################################# START
# Write the results to a file
for review in worker(queue, user_agents):
    write_to_file(review)

# %%

# (nlp_env) alfred@net-g14:~/code/OpenRice/openrice_recommendator$ nohup python scrape_bs_mt.py > scrape_bs_mt.out 2>&1 &
# (nlp_env) alfred@net-g14:~/code/OpenRice/openrice_recommendator$ less scrape_bs_mt.out 