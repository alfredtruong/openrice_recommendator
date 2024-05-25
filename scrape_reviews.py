#%%
import logging # self.log(thing,logging.WARN)
import pandas as pd
import json
import math
import csv
import random
#import fcntl
#import portalocker


import scrapy
from scrapy.crawler import CrawlerProcess 
from scrapy.utils.response import open_in_browser # open_in_browser(response)
from scrapy.shell import inspect_response # inspect_response(response, self)
# view(response) within scrapy.shell
# fake to become a browser
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

# get urls
ALL_REVIEW_URLS_OUT = 'assets/all_review_urls.csv'
review_urls = pd.read_csv(ALL_REVIEW_URLS_OUT,header=None)[0].to_list()

#%%
# utility function
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('assets/scrapes/output2.jl', 'w', encoding='utf-8-sig')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

#%%

# extraction function
class OpenriceSpider(scrapy.Spider):
    name = "openrice"
    start_urls = review_urls

    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'FEED_URI': '/home/alfred/code/OpenRice/openrice_recommendator/assets/scrapes/output3.jsonl',
        'FEED_EXPORT_ENCODING': 'utf-8',
        #'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'RETRY_TIMES': 2,
        'RETRY_HTTP_CODES': [429, 503],
        'DOWNLOAD_TIMEOUT': 3,
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': random.uniform(1, 2),
        'CONCURRENT_REQUESTS': 10,
        'CONCURRENT_REQUESTS_PER_IP': 5,
    }

    user_agents = [
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = []
        #self.load_visited_urls()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers={'User-Agent': random.choice(self.user_agents)})

    def parse(self, response):
        self.log(response.url,logging.WARN)
        reviews = response.xpath('//*[@id="sr2-review-container"]')
        for review in reviews:
            yield {
                # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
                'url': response.url,
                'review': review.xpath('div[2]/div[1]/div[2]/section/div[2]/div[2]/div/section/text()').extract(),
            }


    '''
    def load_visited_urls(self):
        try:
            with open(VISITED_URLS_FILE, 'r') as f:
                self.visited_urls = [line.strip() for line in f]
        except FileNotFoundError:
            pass
    '''
    '''
    # concurrent
    def save_visited_urls(self):
        try:
            with open(VISITED_URLS_FILE, 'a') as f:
                portalocker.lock(f, portalocker.LOCK_EX) # Acquire an exclusive lock on the file
                # Write the URLs to the file
                for url in self.visited_urls:
                    f.write(url + '\n')
                portalocker.unlock(f) # Release the lock
        except Exception as e:
            self.logger.error(f"Error saving visited URLs: {e}")
    '''
c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
})

c.crawl(OpenriceSpider)
c.start()
'''
# non-concurrent
def save_visited_urls(self):
    with open(VISITED_URLS_FILE, 'a') as f:
        for url in self.visited_urls:
            f.write(url + '\n')
'''
'''
# concurrent
def save_visited_urls(self):
    try:
        with open(VISITED_URLS_FILE, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX) # Acquire an exclusive lock on the file
            # Write the URLs to the file
            for url in self.visited_urls:
                f.write(url + '\n')

            fcntl.flock(f, fcntl.LOCK_UN) # Release the lock
            
    except Exception as e:
        self.logger.error(f"Error saving visited URLs: {e}")
'''
#%%

# (nlp_env) alfred@net-g14:~/code/OpenRice/openrice_recommendator$ nohup python scrape_reviews.py > scrape_reviews.out 2>&1 &
# (nlp_env) alfred@net-g14:~/code/OpenRice/openrice_recommendator$ less scrape_reviews.out 