'''
given district
grab all restaurants in this district
build all review urls
'''

#%%
import requests
import json
import math
import pandas as pd
import os
import random
import time
from typing import Dict

from openrice_referentials import *
# fake to become a browser
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

PROD = True
TESTING = False

#%%
# search key
def skey(searchKey):
    return searchKey.split('=')[0]

# search value
def sval(searchKey):
    return searchKey.split('=')[1]

'''
def get_district_page_results(district: int,page_num: int):
    link = f"https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page={page_num}&sortBy=Default&districtId={district}"
    print(link)
    try:
        r = requests.get(link, headers = headers)
        result = json.loads(r.text)
        return result
    except Exception as e:
        print(f'an exception occured',str(e))
        return None
results = get_district_page_results(2008,1)
'''

def request_results_dict(
    page_num: int,
    districtId: int,
    priceRangeId: int = None,
) -> Dict:
    # build json save path
    filepath = f"C:/Users/alfred/Desktop/D_DRIVE/requests"
    filepath = f"D:/LLM/cantollm/OpenRice/jsons/"
    filepath += f"_districtId={districtId}"
    filepath += f"_page={page_num}"
    if priceRangeId is not None: filepath += f"_priceRangeId={priceRangeId}"
    filepath += f".json"
    #print(filepath)

    # return from cache if it exists
    if os.path.exists(filepath):
        print(f'{filepath} exists') # prints this
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
        #print(f'{filepath} doesnt exist')

    # build link
    link = f"https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page={page_num}&sortBy=Default"
    link += f"&districtId={districtId}"
    if priceRangeId is not None: link += f"&priceRangeId={priceRangeId}"
    #link = f"https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page={page_num}&sortBy=Default&districtId={districtId}"
    print(link) # or this

    if PROD or TESTING:
        # do request
        try:
            # get and convert
            r = requests.get(link, headers = headers) # get
            result = json.loads(r.text) # convert
            with open(filepath,'w',encoding='utf-8') as f: json.dump(result,f) # save
            #print(f'\trequest success') # done
            return result # return
        except Exception as e:
            print(f'\trequest failure',str(e)) # failure
            return None
# request_results_dict(0,2008)

# given results, extract what we want into a dataframe
def build_df_from_results_dict(results_dict: Dict[str,object]) -> pd.DataFrame:
    # extract
    restaurant_results = results_dict['searchResult']['paginationResult']['results']
    filter_total = results_dict['searchResult']['paginationResult']['count']
    max_returnable = results_dict['searchResult']['paginationResult']['totalReturnCount']

    print(f"filter_total = {filter_total}, max_returnable = {max_returnable}, this_page = {results_dict['page']}, max_page = {results_dict['totalPage']}, page_results_count = {len(restaurant_results)}, page_rows = {results_dict['rows']}")

    # stop if no result
    if len(restaurant_results) == 0:
        return None
    
    try:
        # loop over restaurants
        df = pd.DataFrame(
            {
                'name': [r['nameUI'].encode('utf-8') for r in restaurant_results],
                'url': [r['urlUI'] for r in restaurant_results], # hyperlink of review
                'review_url': [r['reviewUrlUI'] for r in restaurant_results], # hyperlink of review
                'district': [r['district']['name'] for r in restaurant_results],
                'district_id': [r['district']['districtId'] for r in restaurant_results],
                'districtId': [r['district']['searchKey'] for r in restaurant_results],
                'priceUI': [r['priceUI'] for r in restaurant_results],
                'priceRangeId': [r['priceRangeId'] for r in restaurant_results],
                'photoCount': [r['photoCount'] for r in restaurant_results], # count of reviews
                'review_count': [r['reviewCount'] for r in restaurant_results], # count of reviews
                'bookmark_count': [r['bookmarkedUserCount'] for r in restaurant_results], # how many users have bookmarked
            }
        )
        return df
    except Exception as e:
        print(f'[build_df_from_results_dict] {e}')
        return None
# build_df_from_results_dict(results)

# given df, save it
def add_df_restauraunts_to_csv(
    df: pd.DataFrame,
    districtId: int,
    priceRangeId: int = None,
):
    # build csv filepath
    filepath = f"assets/restaurants/restaurants"
    filepath += f"_districtId={districtId}"
    if priceRangeId is not None: filepath += f"_priceRangeId={priceRangeId}"
    filepath += f".csv"

    with open(filepath, 'a') as f:
        df.to_csv(filepath, mode='a', header=f.tell()==0,index=False)

def request_scrape_and_save_restaurants_one_page(
    page_num: int,
    districtId: int,
    priceRangeId: int = None,
) -> int :
    if PROD or TESTING: time.sleep(random.uniform(0.25,2))
    results_dict = request_results_dict(
        page_num=page_num,
        districtId=districtId,
        priceRangeId=priceRangeId,
    )
    if results_dict is None:
        return 0

    df = build_df_from_results_dict(results_dict=results_dict)
    if df is None:
        return 0

    add_df_restauraunts_to_csv(
        df=df,
        districtId=districtId,
        priceRangeId=priceRangeId,
    )

    # restaurants_in_this_response
    return len(df) 


def request_scrape_and_save_restaurants_all_pages(
    districtId: int,
    priceRangeId: int = None,
) -> int:
    tot_results = 0
    for page_num in range(1,20):
        num_results = request_scrape_and_save_restaurants_one_page(
            page_num=page_num,
            districtId=districtId,
            priceRangeId=priceRangeId
        )
        if num_results > 0:
            tot_results += num_results
        else:
            break

    return tot_results

#%%

if TESTING: INPUT_DF = districts_df[:5]
if PROD: INPUT_DF = districts_df[5:]
if PROD: INPUT_DF = districts_df[35:]
if PROD: INPUT_DF = districts_df[53:]
if PROD: INPUT_DF = districts_df[61:]

# scrape for couple of rows
for idx,district_row in INPUT_DF.iterrows():
    district_searchkey = district_row['searchKey']
    district_id = sval(district_searchkey)
    district_name = district_row['name']
    district_count = int(district_row['count'])
    if district_id not in ['1999','2999','3999','4999']: # look at actual district, not mega-region
        if district_count <= 250:
            # single district gives 250 results, less than so can paginate without price
            tot_results = request_scrape_and_save_restaurants_all_pages(districtId=district_id)
            print(f'[{district_searchkey}] got {tot_results} of {district_count}')
        else:
            tot_results = 0
            # single district gives 250 results, more than so need request with price as well
            for pricerange in priceranges:
                num_results = request_scrape_and_save_restaurants_all_pages(districtId=district_id,priceRangeId=sval(pricerange))
                tot_results += num_results
            print(f'[{district_searchkey}] got {tot_results} of {district_count}')

#%%

