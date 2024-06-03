#%%
import logging # self.log(thing,logging.WARN)
import pandas as pd
import json
import math
import csv
import random
import requests
from bs4 import BeautifulSoup  

################################# PARAMS
from scrape_params import user_agents
ALL_REVIEW_URLS_OUT = 'assets/all_review_urls.csv'
review_urls = pd.read_csv(ALL_REVIEW_URLS_OUT,header=None)[0].to_list()

#%%

#for url in review_urls[:2]: print(url)


# Function to scrape a single URL
def scrape_url(url):
    # Rotate User Agent
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}

    # Send request and get response
    response = requests.get(url, headers=headers)

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract review data
    reviews = soup.find_all('div', {'class': 'tab-pane content content-full js-content-full'})
    print(len(reviews))

    for review in reviews:
        review_container = review.find('section', {'class': 'review-container'})
        for element in review_container.find_all('a'):
            element.decompose()
        if review_container:
            yield {
                'url': url,
                'review': review_container.get_text(strip=True)
            }

def write_to_file(entry):
    with open('assets/scrapes/output_bs.jsonl', 'a', encoding='utf-8') as f:
        line = json.dumps(dict(entry),ensure_ascii=False) + "\n"
        f.write(line)

# Loop over review URLs and scrape each one
for url in review_urls[:2]:
    for review in scrape_url(url):
        # Process each review data
        print(review)
        # You can also write it to a file or database
        write_to_file(review)


# %%
