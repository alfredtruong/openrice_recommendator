#%%
import logging # self.log(thing,logging.WARN)
import pandas as pd
import json
import math
import csv
import random
#import fcntl
import portalocker


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
        self.file = open('openrice.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

#%%

## USE THIS ONE

#VISITED_URLS_FILE = 'assets/all_review_urls_visited.txt'
# extraction function
class OpenriceSpider(scrapy.Spider):
    name = "openrice"
    start_urls = review_urls

    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'data/output.jsonl',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_TIMES': 1,
        'RETRY_HTTP_CODES': [429, 503],
        'DOWNLOAD_TIMEOUT': 2,
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': random.uniform(1,2),
        'CONCURRENT_REQUESTS': 50,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = []
        #self.load_visited_urls()

    def parse(self, response):
        #open_in_browser(response) # tell scrapy to open this page in a browser
        #inspect_response(response, self) # inspect response object
        #user_blocks = response.xpath('//*[@class="sr2-review-list-container full clearfix js-sr2-review-list-container"]')
        #self.visited_urls.append(response.url) # Add current URL to visited URLs
        self.log(response.url,logging.WARN)
        reviews = response.xpath('//*[@id="sr2-review-container"]')
        for review in reviews:
            #breakpoint()
            yield {
                # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
                'url': response.url,
                'review': review.xpath('div[2]/div[1]/div[2]/section/div[2]/div[2]/div/section/text()').extract(),
            }

        #self.save_visited_urls() # Save visited URLs to file

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



# DONT USE THIS ONE
import os
import re
import json
import scrapy
import datetime

class OpenriceSpider(scrapy.Spider):
    name = "openrice"
    start_urls = review_urls

    custom_settings = {
        'FEEDS': { # not used
            'data/%(filename)s_%(time)s.jsonl': { # not used
                'format': 'jsonlines', # not used
                'overwrite': False, # not used
                } # not used
        }, # not used
        'FEED_EXPORT_ENCODING': 'utf-8', # not used
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # is used
        'RETRY_TIMES': 1,
        'RETRY_HTTP_CODES': [429, 503],
        'DOWNLOAD_TIMEOUT': 2,
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': random.uniform(1, 2),
        'CONCURRENT_REQUESTS': 100,
    }

    def get_filename(self, response):
        url = response.url
        url = url.replace('.', '_')
        url = url.replace('/', '_')
        return f"{url}.jsonl"

    '''
    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'data/output.jsonl',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_TIMES': 1,
        'RETRY_HTTP_CODES': [429, 503],
        'DOWNLOAD_TIMEOUT': 2,
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': random.uniform(1,2),
        'CONCURRENT_REQUESTS': 100,
    }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def parse(self, response):
        self.log(response.url,logging.WARN)
        reviews = response.xpath('//*[@id="sr2-review-container"]')
        for review in reviews:
            yield {
                'url': response.url,
                'review': review.xpath('div[2]/div[1]/div[2]/section/div[2]/div[2]/div/section/text()').extract(),
            }

    '''
    def close(self, reason):
        for url in self.start_urls:
            clean_url = re.sub(r'[^a-zA-Z0-9_\-]+', '', url)
            filename = os.path.join("data", f"{self.name}_{clean_url}_{self.start_time}.jsonl")
            response = scrapy.Response(url=url)
            data = [{'url': url, 'reviews': [x for x in self.parse(response)]}]
            with open(filename, 'w') as f:
                json.dump(data, f)
    '''

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
})

c.crawl(OpenriceSpider)
c.start()

#%%
