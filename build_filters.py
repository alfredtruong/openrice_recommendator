'''
use api to get restaurants
'''

'''
# uses .venv
pip install requests
pip install pandas
'''
#%%
import requests
import json
import pandas as pd

#%%
# fake to become a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

'''
#%%
# get data
page_num = 0
link = f"https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page={page_num}&&sortBy=Default"
r = requests.get(link, headers = headers)
result = json.loads(r.text)
result.keys()

['searchResult', 
'title', # Hong Kong Restaurant Search  | OpenRice Hong Kong
'startAt' # 0
'rows' # 15
'totalPage' # 17
'page' # 1
'mapSearchUrlUI' # /en/hongkong/restaurants?mapType=1
'listSearchUrlUI' # /en/hongkong/restaurants
'nearBySearchUrlUI' # /en/hongkong/nearby-restaurants
'closedPoiCount' # 0
'baseUrl', # baseUrl /en/hongkong/restaurants
'mobilePagination', # useless
'desktopPagination', # useless
'pageInfo' # useless
]
"""

#%%

result['searchResult']['refineSearchFilter'].keys()

[
    'currencyCodeUI', # useless
    'bookmarkedOnlyUI', # useless
    'sortByTypes', # useless
    'cuisines',
    'themes',
    'features',
    'offers',
    'locations',
    'foodTypes',
    'keywords',
    'bookings',
    'bizServices',
    'priceRanges',
    'statuses',
    'bookmarkedCategories',
    'hideItemsOfSearchKeys'
]
'''


for filter in ['cuisines','themes','locations','foodTypes','priceRanges']:
    for k,v in result['searchResult']['refineSearchFilter'][filter][0].items():
        print(f'{filter}\t{k}\t{v}')

for filter in result['searchResult']['refineSearchFilter'].keys():
    try:
        for k,v in result['searchResult']['refineSearchFilter'][filter][0].items():
            print(f'{filter}\t{k}\t{v}')
    except:
        pass

'''
sortByTypes	value	0
sortByTypes	queryKey	sortBy
sortByTypes	queryValue	Default
sortByTypes	searchKey	sortBy=Default
sortByTypes	type	3
sortByTypes	name	Overall (High to Low)
sortByTypes	selected	False
sortByTypes	id	0
sortByTypes	hide	False
sortByTypes	showInCurrentFilterSection	True
    cuisines	aliasUI	港式||Hong Kong Style                       #######
    cuisines	value	0
    cuisines	queryKey	cuisineId                               #######
    cuisines	queryValue	1004                                    #######
    cuisines	searchKey	cuisineId=1004                          #######
    cuisines	type	10
    cuisines	name	Hong Kong Style
    cuisines	count	11399                                       #######
    cuisines	selected	False
    cuisines	id	1004
    cuisines	showAlways	False
    cuisines	isEnabled	True
    cuisines	loginRequired	False
    cuisines	nameLangDict	{}
    cuisines	locationRequired	False
    cuisines	hide	False
    cuisines	exclusiveFilterIds	[]
    cuisines	showInCurrentFilterSection	True
themes	aliasUI	飲o野傾計||Casual Drink||饮o野倾计
themes	value	0
themes	queryKey	themeId
themes	queryValue	11
themes	searchKey	themeId=11
themes	type	13
themes	name	Casual Drink
themes	count	405
themes	selected	False
themes	id	11
themes	showAlways	False
themes	isEnabled	True
themes	loginRequired	False
themes	nameLangDict	{}
themes	locationRequired	False
themes	hide	False
themes	exclusiveFilterIds	[]
themes	showInCurrentFilterSection	True
features	styleUI	Condition_opennow
features	value	0
features	queryKey	conditionId
features	queryValue	2013
features	searchKey	conditionId=2013
features	type	19
features	name	Open Now
features	count	0
features	selected	False
features	id	2013
features	icon	https://static8.orstatic.com/images/v5/android/filter/filter_open.png?90
features	showAlways	True
features	isEnabled	True
features	loginRequired	False
features	nameLangDict	{}
features	locationRequired	False
features	hide	False
features	exclusiveFilterIds	[]
features	showInCurrentFilterSection	True
offers	styleUI	Offer_haveBookingOffer
offers	value	0
offers	queryKey	haveBookingOffer
offers	queryValue	true
offers	searchKey	haveBookingOffer=true
offers	type	47
offers	name	Booking Offer
offers	count	3885
offers	selected	False
offers	icon	https://static7.orstatic.com/images/v5/android/filter/filter_booking.png?90
offers	showAlways	False
offers	isEnabled	True
offers	loginRequired	False
offers	nameLangDict	{}
offers	locationRequired	False
offers	hide	False
offers	exclusiveFilterIds	[]
offers	showInCurrentFilterSection	True
    locations	aliasUI	九龍||Kowloon||九龙
    locations	value	0
    locations	filter	district
    locations	queryKey	districtId
    locations	queryValue	2999
    locations	searchKey	districtId=2999
    locations	type	8
    locations	name	Kowloon
    locations	count	12370
    locations	selected	False
    locations	id	2999
    locations	showAlways	False
    locations	isEnabled	True
    locations	loginRequired	False
    locations	nameLangDict	{}
    locations	locationRequired	False
    locations	hide	False
    locations	exclusiveFilterIds	[]
    locations	showInCurrentFilterSection	True
        foodTypes	aliasUI	港式||Hong Kong Style
        foodTypes	value	0
        foodTypes	queryKey	categoryGroupId
        foodTypes	queryValue	20009
        foodTypes	searchKey	categoryGroupId=20009
        foodTypes	type	14
        foodTypes	name	Hong Kong Style
        foodTypes	count	9106
        foodTypes	selected	False
        foodTypes	hide	False
        foodTypes	showInCurrentFilterSection	True
bizServices	type	43
bizServices	name	Booking
bizServices	searchKey	tmReservation=true
bizServices	selected	False
bizServices	icon	https://static7.orstatic.com/images/v5/android/filter/filter_booking.png?90
bizServices	showAlways	True
bizServices	isEnabled	True
bizServices	loginRequired	False
bizServices	nameLangDict	{}
bizServices	locationRequired	False
bizServices	hide	False
bizServices	exclusiveFilterIds	[]
bizServices	showInCurrentFilterSection	True
priceRanges	type	15
priceRanges	name	0
priceRanges	searchKey	priceRangeId=1
priceRanges	selected	True
priceRanges	id	1
priceRanges	hide	False
priceRanges	showInCurrentFilterSection	True
statuses	type	35
statuses	name	10
statuses	searchKey	status=10
statuses	count	29417
statuses	selected	False
statuses	id	10
statuses	showAlways	False
statuses	isEnabled	True
statuses	loginRequired	False
statuses	nameLangDict	{}
statuses	locationRequired	False
statuses	hide	False
statuses	exclusiveFilterIds	[]
statuses	showInCurrentFilterSection	True
'''

#%%
################# REQUEST DATA
def get_page_results(page_num: int):
    link = f"https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page={page_num}&&sortBy=Default"
    print(link)
    r = requests.get(link, headers = headers)
    result = json.loads(r.text)
    return result

################# SAVER
def save_type_to_csv(type: str, page_num: int, df):
    filename = f"assets/data/type_{type}_page_{page_num}.csv"
    print(filename)
    with open(filename, 'a') as f:
        df.to_csv(filename, mode='a', encoding='utf-8-sig', header=f.tell()==0,index=False)

################# LOCATION
'''
locations	aliasUI	九龍||Kowloon||九龙
locations	value	0
locations	filter	district
locations	queryKey	districtId
locations	queryValue	2999
locations	searchKey	districtId=2999
locations	type	8
locations	name	Kowloon
locations	count	12370
locations	selected	False
locations	id	2999
locations	showAlways	False
locations	isEnabled	True
locations	loginRequired	False
locations	nameLangDict	{}
locations	locationRequired	False
locations	hide	False
locations	exclusiveFilterIds	[]
locations	showInCurrentFilterSection	True
'''
def result_locations_to_df(result):
    # info
    info = result['searchResult']['refineSearchFilter']['locations']
    #print(info.keys())

    # strip
    df = pd.DataFrame(
        {
            'aliasUI' : [i['aliasUI'] for i in info], # location alias
            'Count' : [i['count'] for i in info], # number within this location grouping
            'Type' : [i['queryKey'] for i in info], # type of grouping
            'ID' : [i['queryValue'] for i in info], # identifier for this grouping
            'Name' : [i['name'] for i in info], # location name
            'Search Key' : [i['searchKey'] for i in info], # how to access this grouping
        } 
    )
    return df

################# CUISINE
'''
cuisines	aliasUI	港式||Hong Kong Style                       #######
cuisines	value	0
cuisines	queryKey	cuisineId                               #######
cuisines	queryValue	1004                                    #######
cuisines	searchKey	cuisineId=1004                          #######
cuisines	type	10
cuisines	name	Hong Kong Style
cuisines	count	11399                                       #######
cuisines	selected	False
cuisines	id	1004
cuisines	showAlways	False
cuisines	isEnabled	True
cuisines	loginRequired	False
cuisines	nameLangDict	{}
cuisines	locationRequired	False
cuisines	hide	False
cuisines	exclusiveFilterIds	[]
cuisines	showInCurrentFilterSection	True
'''
def result_cuisines_to_df(result):
    # info
    info = result['searchResult']['refineSearchFilter']['cuisines']
    #print(info.keys())
    # strip
    df = pd.DataFrame(
        {
            'aliasUI' : [i['aliasUI'] for i in info], # location alias
            'Count' : [i['count'] for i in info], # number within this location grouping
            'Type' : [i['queryKey'] for i in info], # type of grouping
            'ID' : [i['queryValue'] for i in info], # identifier for this grouping
            'Name' : [i['name'] for i in info], # location name
            'Search Key' : [i['searchKey'] for i in info], # how to access this grouping
        } 
    )
    return df

################# FOODTYPES
'''
foodTypes	aliasUI	港式||Hong Kong Style
foodTypes	value	0
foodTypes	queryKey	categoryGroupId
foodTypes	queryValue	20009
foodTypes	searchKey	categoryGroupId=20009
foodTypes	type	14
foodTypes	name	Hong Kong Style
foodTypes	count	9106
foodTypes	selected	False
foodTypes	hide	False
foodTypes	showInCurrentFilterSection	True
'''
def result_foodtypes_to_df(result):
    # info
    info = result['searchResult']['refineSearchFilter']['foodTypes']
    #print(info.keys())
    # strip
    df = pd.DataFrame(
        {
            'aliasUI' : [i['aliasUI'] for i in info], # location alias
            'Count' : [i['count'] for i in info], # number within this location grouping
            'Type' : [i['queryKey'] for i in info], # type of grouping
            'ID' : [i['queryValue'] for i in info], # identifier for this grouping
            'Name' : [i['name'] for i in info], # location name
            'Search Key' : [i['searchKey'] for i in info], # how to access this grouping
        } 
    )
    return df

'''
priceRanges	type	15
priceRanges	name	0
priceRanges	searchKey	priceRangeId=1
priceRanges	selected	True
priceRanges	id	1
priceRanges	hide	False
priceRanges	showInCurrentFilterSection	True
'''
def result_priceranges_to_df(result):
    # info
    info = result['searchResult']['refineSearchFilter']['priceRanges']
    #print(info.keys())
    # strip
    df = pd.DataFrame(
        {
            'Name' : [i['name'] for i in info], # location name
            'Search Key' : [i['searchKey'] for i in info], # how to access this grouping
        } 
    )
    return df
#%%
page_num = 2
result = get_page_results(page_num)

#%%
# locations
locations = result_locations_to_df(result)
save_type_to_csv('locations',page_num,locations)
# cuisines
cuisines = result_cuisines_to_df(result)
save_type_to_csv('cuisines',page_num,cuisines)
# foodtypes
foodtypes = result_foodtypes_to_df(result)
save_type_to_csv('foodtypes',page_num,foodtypes)
# priceranges
priceranges = result_priceranges_to_df(result)
save_type_to_csv('priceranges',page_num,priceranges)

# %%

# results from all pages are the same
