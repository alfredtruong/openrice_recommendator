#%%
import pandas as pd
from pathlib import Path
import glob
import os
import math
import csv
#################### COMBINE ALL RESTAURANTS
ALL_RESTAURANTS_DIR = 'assets/restaurants/'
ALL_RESTAURANTS_OUT = 'assets/all_restaurants.csv'

csv_files = glob.glob(os.path.join(ALL_RESTAURANTS_DIR, "*.csv")) 
print(csv_files)
#%%


# Create an empty dataframe to store the combined data
all_restaurants_df = pd.DataFrame()

# Loop through each CSV file and append its contents to the combined dataframe
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    print(csv_file,len(df))
    all_restaurants_df = pd.concat([all_restaurants_df, df])

# combine and save
all_restaurants_df.drop_duplicates()
all_restaurants_df.to_csv(ALL_RESTAURANTS_OUT,encoding='utf-8-sig',index=False)

#################### COMBINE ALL RESTAURANTS
ALL_REVIEW_URLS_OUT = 'assets/all_review_urls.csv'

#%%
# generate all review subpages
all_review_urls = []
for idx,row in all_restaurants_df.iterrows():
    num_of_review_pages = math.ceil(row['review_count'] / 15) # there are 15 reviews per page
    
    for i in range(1,int(num_of_review_pages)):
        all_review_urls.append(f"https://www.openrice.com{row['review_url']}?page={i}")

# write all urls
with open(ALL_REVIEW_URLS_OUT, 'w', newline='') as f:
    writer = csv.writer(f)
    for review_url in all_review_urls:
        writer.writerow([review_url])
#%%


#%%
# print review_urls
print("There is {} urls to scrape".format(len(all_review_urls)))

#https://www.openrice.com/en/hongkong/r-burgeroom-causeway-bay-american-hamburger-r189507/reviews
#https://www.openrice.com/en/hongkong/r-burgeroom-causeway-bay-american-hamburger-r189507/reviews?page=2
# %%