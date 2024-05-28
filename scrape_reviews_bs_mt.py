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

################################# PARAMS
from scrape_params import user_agents

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