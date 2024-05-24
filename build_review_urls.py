import pandas as pd

df_master = pd.read_csv("assets/data/master_restaurant_urls_AT.csv")

for i in df['Review URL']:
    # https://stackoverflow.com/questions/30944577/check-if-string-is-in-a-pandas-dataframe
    if df_master['Review URL'].str.contains(i).any():
        # https://stackoverflow.com/questions/36684013/extract-column-value-based-on-another-column-pandas-dataframe
        df_master.loc[df_master['Review URL'] == i, 'Smile'] = df.loc[df['Review URL'] == i, 'Smile'].iloc[0]
        df_master.loc[df_master['Review URL'] == i, 'Cry'] = df.loc[df['Review URL'] == i, 'Cry'].iloc[0]
        df_master.loc[df_master['Review URL'] == i, 'Overall Score'] = df.loc[df['Review URL'] == i, 'Overall Score'].iloc[0]
        df_master.loc[df_master['Review URL'] == i, 'Bookmark Count'] = df.loc[df['Review URL'] == i, 'Bookmark Count'].iloc[0]
        df_master.loc[df_master['Review URL'] == i, 'Review Count'] = df.loc[df['Review URL'] == i, 'Review Count'].iloc[0]
        
        # If there's duplicate, reduce the amount of duplicate reviews to scrape
        df.loc[df['Review URL'] == i, 'Review Count'] = df.loc[df['Review URL'] == i, 'Review Count'].iloc[0] - df_master.loc[df_master['Review URL'] == i, 'Review Count'].iloc[0]
    else:
        # https://stackoverflow.com/questions/39815646/pandas-append-dataframe-to-another-df
        df_master = df_master.append(df.loc[df['Review URL'] == i],ignore_index=True)

df_master.to_csv('assets/data/master_restaurant_urls.csv',encoding='utf-8',index=False)


#%%
# generate urls to all review subpages
review_urls = []

for k in range(len(df['Review Count'])):
    num_of_review_pages = math.ceil(df['Review Count'][k] / 15.0) # there are 15 reviews per page

    for i in range(1,int(num_of_review_pages)):
        review_urls.append('https://www.openrice.com'+ str(df['Review URL'][k]) + '?page='+ str( i ))

# print review_urls
print("There is {} urls to scrape".format(len(review_urls)))

#https://www.openrice.com/en/hongkong/r-burgeroom-causeway-bay-american-hamburger-r189507/reviews
#https://www.openrice.com/en/hongkong/r-burgeroom-causeway-bay-american-hamburger-r189507/reviews?page=2
# %%