#%%
import logging # self.log(thing,logging.WARN)
import pandas as pd
import json
import math
import csv
import random
import fcntl

import scrapy
from scrapy.crawler import CrawlerProcess 
from scrapy.utils.response import open_in_browser # open_in_browser(response)
from scrapy.shell import inspect_response # inspect_response(response, self)
# view(response) within scrapy.shell
# fake to become a browser
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

'''
scrapy logging techniques
    https://www.youtube.com/watch?v=5YmyALotdn0

    # import logging
    import logging
    self.log(user)

    # inspect_response()
    import scrapy
scrapy runspider python_script.py
'''
#%%

# get urls
df = pd.read_csv('review_url_AT.csv')
review_restaurant = []
review_page = []
review_urls = []
for k in range(len(df['Review Count'])):
    num_of_review_pages = math.ceil(df['Review Count'][k] / 15.0)

    for i in range(1,int(num_of_review_pages)):
        review_urls.append('https://www.openrice.com'+ str(df['Review URL'][k]) + '?page='+ str( i ))
        review_restaurant.append(df['Name'])
        review_page.append(i)

with open('urls_to_scrape_AT.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for review_url in review_urls:
        writer.writerow([review_url])

print("There is {} urls to scrape".format(len(review_urls)))
#%%

# utility function
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('reviewresult_AT.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

#%%
VISITED_URLS_FILE = 'visited_urls.txt'

# extraction function
class OpenriceSpider(scrapy.Spider):
    name = "openrice"
    start_urls = review_urls

    custom_settings = { 
        'LOG_LEVEL': logging.WARNING,
        'FEEDS': {
            'data/%(filename)s_%(time)s.jsonl': {
                'format': 'jsonlines', 
                'overwrite': False,
                }
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [429, 503],
        'DOWNLOAD_TIMEOUT': 2,
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': random.uniform(1, 2),
        'CONCURRENT_REQUESTS': 10,
    }
    '''
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'reviewresult.json'                       # Used for pipeline 2
    }
    '''

    def get_filename(self, response):
        url = response.url
        url = url.replace('.', '_')
        url = url.replace('/', '_')
        return f"{url}.jsonl"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = []
        self.load_visited_urls()

    def load_visited_urls(self):
        try:
            with open(VISITED_URLS_FILE, 'r') as f:
                self.visited_urls = [line.strip() for line in f]
        except FileNotFoundError:
            pass
    
    def parse(self, response):
        #open_in_browser(response) # tell scrapy to open this page in a browser
        #inspect_response(response, self) # inspect response object
        #user_blocks = response.xpath('//*[@class="sr2-review-list-container full clearfix js-sr2-review-list-container"]')
        self.visited_urls.append(response.url) # Add current URL to visited URLs
        self.log(response.url,logging.WARN)
        reviews = response.xpath('//*[@id="sr2-review-container"]')
        for review in reviews:
            #breakpoint()
            yield {
                # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
                'url': response.url,
                'review': review.xpath('div[2]/div[1]/div[2]/section/div[2]/div[2]/div/section/text()').extract(),
            }

        self.save_visited_urls() # Save visited URLs to file

    '''
    # non-concurrent
    def save_visited_urls(self):
        with open(VISITED_URLS_FILE, 'a') as f:
            for url in self.visited_urls:
                f.write(url + '\n')
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

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
})

c.crawl(OpenriceSpider)
c.start()

#%%
