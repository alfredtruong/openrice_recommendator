# Openrice Review Scraper
code to extract text reviews from Openrice website
approach taken

1) use [api](https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong) to extract restaurants
    - extract filters (`build_filters.py`)
        api returns at most 250 results regardless of total results
    - use api + filters to extract restaurant main pages (`build_restaurant_urls.py`)
        apply multiple filters to get results if total > 250 results

2) build link to restaurant review subpages (`build_review_urls.py`)
    - Openrice webpage returns at most 15 reviews per page

3) use BeautifulSoup to scrape reviews
    - sleep to be nice
    - use proxy-list + multi-threading to not take forever