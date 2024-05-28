# https://hasdata.com/blog/best-free-proxies-for-web-scraping

#%%
################# IMPORTS
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup  
import os
import queue
import random
import time
import threading

################# FUNCTIONS
def is_already_processed(file_path,url):
    with lock:
        ans = False
        try:
            with open(file_path, 'r') as f:
                if url in set(line.strip() for line in f):
                    ans = True
        except FileNotFoundError:
            pass

        if ans:
            if TESTING: 
                print(f"[{url}] already processed, skipping...")
            else:
                print('x')
        else:
            if TESTING:
                print(f"[{url}] not processed, do now")
            else:
                print('.')
        return ans


def write_url_to_file(file_path, url):
    with lock:
        with open(file_path, 'a') as f:
            f.write(url + '\n')

# Define a thread worker function
def worker(identifier, queue, user_agents, proxy_list):
    print(identifier)
    while True:
        # get url
        url = queue.get()
        if url is None:  # poison pill, exit the thread
            break

        if is_already_processed(PROCESSED_URLS,url):
            continue

        # standard sleep
        short_wait = random.uniform(WAIT_MIN_SHORT, WAIT_MAX_SHORT)
        long_wait = 0
        time.sleep(short_wait)
        if random.random() < 0.2:
            long_wait = random.uniform(WAIT_MIN_LONG, WAIT_MAX_LONG)
            time.sleep(long_wait)

        if TESTING: print(short_wait,long_wait)
        # prep request
        headers = {'User-Agent': random.choice(user_agents)} # user_agent
        proxies = {'http': random.choice(proxy_list)} # proxy_pool

        # print(headers,proxies)
        # get data
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            write_url_to_file(SKIPPED_URLS,url)
            continue

        # extract reviews
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 'tab-pane content content-full js-content-full'})
        entrys = []
        for review in reviews:
            # grab container
            review_container = review.find('section', {'class': 'review-container'})

            # remove 
            for element in review_container.find_all('a'):
                element.decompose()
            
            entry = {
                    'url': url,
                    'review': review_container.get_text(strip=True)
            }
            entrys.append(entry)
            '''
            if review_container:
                yield {
                    'url': url,
                    'review': review_container.get_text(strip=True)
                }
            '''
        write_entrys_to_file(entrys)

        # Save the URL to the processed_urls file
        write_url_to_file(PROCESSED_URLS, url)

def write_to_file(entry):
    with lock:
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            line = json.dumps(dict(entry), ensure_ascii=False) + "\n"
            f.write(line)

def write_entrys_to_file(entrys):
    with lock:
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            for entry in entrys:
                line = json.dumps(dict(entry), ensure_ascii=False) + "\n"
                f.write(line)


#%%
################################# PARAMS
from scrape_params import user_agents,proxy_list

################################# SETTINGS
ALL_REVIEW_URLS_OUT = 'assets/all_review_urls.csv'
OUTPUT_FILE = 'assets/scrapes/bs2/output_bs.jsonl'
PROCESSED_URLS = 'assets/scrapes/bs2/output_bs_processed_urls.txt'
SKIPPED_URLS = 'assets/scrapes/bs2/output_bs_skipped_urls.txt'
TESTING = False
TEST_MAX_URLS = 150
WORKERS = 50
WAIT_MIN_SHORT, WAIT_MAX_SHORT = 5, 10
WAIT_MIN_LONG, WAIT_MAX_LONG = 60, 120

#%%
################################# POPULATE QUEUE
# Create a queue to hold the URLs to be scraped
queue = queue.Queue() # for worker args

# Add URLs to the queue
review_urls = pd.read_csv(ALL_REVIEW_URLS_OUT,header=None)[0].to_list()
if TESTING: review_urls = review_urls[:TEST_MAX_URLS] # cut short if testing or not
for url in review_urls: queue.put(url) # populate actual jobs
for _ in range(WORKERS): queue.put(None) # poison pills to the queue to signal threads to exit

################################# POPULATE THREADS
# Create a list to hold the threads
lock = threading.Lock()
threads = []

# Create and start the threads
for identifier in range(WORKERS):
    t = threading.Thread(target=worker, args=(identifier, queue, user_agents, proxy_list))
    t.start()
    threads.append(t)

'''
# Wait for all threads to finish
for t in threads:
    t.join()
'''