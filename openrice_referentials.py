import pandas as pd

'''
r = requests.get("https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page="+ str(i) +"&&sortBy=Default&districtId=2008", headers = headers)
result = json.loads(r.text)

result['searchResult']['paginationResult']['results'] # list of results
len(result['searchResult']['paginationResult']['results']) # 15 results
for k,v in result['searchResult']['paginationResult']['results'][0].items(): print(k,"#",v) # show contents of results
'''
#https://www.openrice.com/en/hongkong/restaurants?sortBy=ORScoreDesc&districtId=2008&cuisineId=4000&tabIndex=0&tabType=
#https://www.openrice.com/api/pois?uiLang=en&uiCity=hongkong&page=1&districtId=2008&cuisineId=4000

#%%

priceranges = [s.split(',')[0] for s in 
'''
priceRangeId=1
priceRangeId=2
priceRangeId=3
priceRangeId=4
priceRangeId=5
priceRangeId=6
'''.strip('\n').split('\n')]

#location
districts_df = pd.DataFrame.from_records([s.split(',') for s in 
'''
districtId=1001,Sheung Wan,536
districtId=1002,The Peak,40
districtId=1003,Central,1536
districtId=1004,North Point,575
districtId=1005,Mid-Levels,78
districtId=1007,Shek O,28
districtId=1008,Western District,797
districtId=1009,Sai Wan Ho,188
districtId=1010,Stanley,56
districtId=1011,Admiralty,196
districtId=1012,Aberdeen,257
districtId=1013,Chai Wan,301
districtId=1014,Quarry Bay,305
districtId=1015,Repulse Bay,28
districtId=1016,Deep Water Bay,13
districtId=1017,Happy Valley,137
districtId=1018,Shau Kei Wan,237
districtId=1019,Causeway Bay,1302
districtId=1020,Ap Lei Chau,149
districtId=1021,Pok Fu Lam,76
districtId=1022,Wan Chai,1244
districtId=1023,Tai Koo,228
districtId=1024,Heng Fa Chuen,41
districtId=1025,Tai Hang,97
districtId=1026,Tin Hau,210
districtId=1027,Wong Chuk Hang,180
districtId=2001,Kowloon City,504
districtId=2002,Kowloon Tong,137
districtId=2003,Kowloon Bay,570
districtId=2004,To Kwa Wan,453
districtId=2005,Tai Kok Tsui,507
districtId=2006,Ngau Tau Kok,182
districtId=2007,Shek Kip Mei,107
districtId=2008,Tsim Sha Tsui,2119
districtId=2009,Ho Man Tin,110
districtId=2010,Mong Kok,1332
districtId=2011,Yau Ma Tei,301
districtId=2012,Yau Tong,129
districtId=2013,Cheung Sha Wan,447
districtId=2015,Hung Hom,687
districtId=2016,Lai Chi Kok,351
districtId=2019,Sham Shui Po,835
districtId=2020,Wong Tai Sin,239
districtId=2021,Tsz Wan Shan,99
districtId=2022,San Po Kong,338
districtId=2024,Lam Tin,177
districtId=2025,Lei Yue Mun,41
districtId=2026,Kwun Tong,1267
districtId=2027,Diamond Hill,108
districtId=2028,Jordan,608
districtId=2029,Prince Edward,437
districtId=2030,Lok Fu,97
districtId=2031,Mei Foo,110
districtId=2032,Choi Hung,78
districtId=3001,Sheung Shui,348
districtId=3002,Tai Po,677
districtId=3003,Yuen Long,1519
districtId=3004,Tin Shui Wai,422
districtId=3005,Tuen Mun,1415
districtId=3006,Sai Kung,317
districtId=3007,Sha Tin,914
districtId=3008,Fanling,410
districtId=3009,Ma On Shan,347
districtId=3010,Sham Tseng,47
districtId=3011,Lo Wu,5
districtId=3012,Tai Wai,348
districtId=3013,Fo Tan,171
districtId=3014,Tai Wo,63
districtId=3015,Kwai Fong,348
districtId=3016,Lau Fau shan,35
districtId=3017,Tsing Yi,266
districtId=3018,Tsuen Wan,1467
districtId=3019,Kwai Chung,613
districtId=3020,Tseung Kwan O,852
districtId=3021,Lok Ma Chau,8
districtId=3022,Ma Wan,41
districtId=-35242,Kennedy Town,228
districtId=-35243,Shek Tong Tsui,176
districtId=-35244,Sai Ying Pun,365
districtId=-35259,Hang Hau,179
districtId=-35260,Po Lam,225
districtId=-35276,O’South Coast,28
districtId=4001,Lantau Island,123
districtId=4002,Chek Lap Kok,155
districtId=4003,Peng Chau,37
districtId=4004,Cheung Chau,211
districtId=4005,Lamma Island,78
districtId=4006,Discovery Bay,51
districtId=4009,Tung Chung,226
districtId=4010,Tai O,72
districtId=4011,Po Toi Island,8
districtId=-9006,Soho,232
districtId=-9007,Lan Kwai Fong,149
districtId=-9151,Cyberport,30
'''.strip('\n').split('\n')],columns=['searchKey','name','count'])

cuisines_df = pd.DataFrame.from_records([s.split(',') for s in 
'''
cuisineId=1001,Chiu Chow,528
cuisineId=1002,Guangdong,3652
cuisineId=1003,Yunnan,398
cuisineId=1004,Hong Kong Style,11399
cuisineId=1005,Hakka,86
cuisineId=1007,Jiang-Zhe,23
cuisineId=1008,Sichuan,973
cuisineId=1009,Taiwan,1571
cuisineId=1010,Beijing,65
cuisineId=1011,Shanghai,410
cuisineId=1012,Fujian,35
cuisineId=1013,Hunan,125
cuisineId=1014,Mongolia,10
cuisineId=1015,Xinjiang,14
cuisineId=1016,Northeastern,34
cuisineId=1017,Guizhou,14
cuisineId=1018,Jingchuanhu,124
cuisineId=1021,Shandong,24
cuisineId=1024,Hubei,1
cuisineId=1026,Guangxi,37
cuisineId=1027,Village Food,13
cuisineId=1030,Shanxi (Jin),26
cuisineId=1031,Shanxi (Shan),11
cuisineId=1032,Huaiyang,5
cuisineId=1033,Shunde,36
cuisineId=2001,Korean,565
cuisineId=2002,Vietnamese,373
cuisineId=2003,Philippines,46
cuisineId=2004,Thai,946
cuisineId=2005,Singaporean,219
cuisineId=2006,Indian,208
cuisineId=2007,Indonesian,42
cuisineId=2008,Nepalese,55
cuisineId=2009,Japanese,3909
cuisineId=2010,Sri Lankan,3
cuisineId=2021,Middle Eastern,71
cuisineId=2022,Australian,44
cuisineId=2023,Lebanon,6
cuisineId=2024,Malaysian,158
cuisineId=3001,German,28
cuisineId=3002,Portuguese,19
cuisineId=3004,Swiss,6
cuisineId=3005,Irish,4
cuisineId=3006,Italian,886
cuisineId=3007,Austrian,1
cuisineId=3008,Dutch,7
cuisineId=3009,British,113
cuisineId=3010,French,393
cuisineId=3011,Spanish,87
cuisineId=3012,Mediterranean,65
cuisineId=3013,Belgian,18
cuisineId=3021,Eastern Europe,5
cuisineId=3033,Turkish,53
cuisineId=3034,Greek,4
cuisineId=4000,Western,4787
cuisineId=4001,American,1059
cuisineId=4002,Mexican,42
cuisineId=4003,Cuba,5
cuisineId=4004,Brazilian,4
cuisineId=4005,Argentinian,16
cuisineId=4006,Peruvian,7
cuisineId=5001,African,7
cuisineId=5004,Egyptian,4
cuisineId=5005,Moroccan,4
cuisineId=6000,International,2134
'''.strip('\n').split('\n')],columns=['searchKey','name','count'])

categorygroup_df = pd.DataFrame.from_records([s.split(',') for s in 
'''
categoryGroupId=20001,Buffet,383
categoryGroupId=20002,Chinese Food,6788
categoryGroupId=20003,Japanese Korean Food,3723
categoryGroupId=20004,Hot Pot,1350
categoryGroupId=20005,Dessert,4055
categoryGroupId=20009,Hong Kong Style,9106
categoryGroupId=20010,Noodles,4697
categoryGroupId=20011,BBQ,1865
categoryGroupId=20012,Seafood,1508
categoryGroupId=20013,Coffee/Beverage,4189
categoryGroupId=20014,Bread,3649
categoryGroupId=20018,Fast Food,3116
categoryGroupId=20019,Healthy Food / Vegetarian,2514
categoryGroupId=20020,Entertainment,2804
categoryGroupId=20021,Seasonal/Traditional Food,1157
categoryGroupId=20231,Theme Restaurant,179
categoryGroupId=20232,Salt & Sugar Reduction Restaurants,1272
categoryGroupId=20238,Takeout Restaurant,1102
'''.strip('\n').split('\n')],columns=['searchKey','name','count'])

amenities_df = pd.DataFrame.from_records([s.split(',') for s in 
'''
amenityId=1001,Stir-Fry,1956
amenityId=1002,Takeaway,1102
amenityId=1003,Steak House,411
amenityId=1005,Dim Sum Restaurant,668
amenityId=1006,Western Restaurant,116
amenityId=1007,Fast Food,1649
amenityId=1008,Coffee Shop,2474
amenityId=1009,Tea Restaurant,2907
amenityId=1010,Bar,1247
amenityId=1011,Hotel Restaurant,485
amenityId=1012,Karaoke,91
amenityId=1015,Snack Shop & Deli,2304
amenityId=1016,Dai Pai Dong,345
amenityId=1017,Cyber Cafe,1
amenityId=1018,Outdoor,16
amenityId=1019,Clubbing,2
amenityId=1021,Yoshoku,313
amenityId=1023,Private Kitchen,369
amenityId=1024,Upper-floor Cafe,278
amenityId=1026,Sushi Bar,8
amenityId=1027,Chocolate/Candy Shop,243
amenityId=1028,BBQ Ground,72
amenityId=1029,Tea House,168
amenityId=1030,Club House,142
amenityId=1031,Food Court,204
amenityId=1032,Oyster Bar,84
amenityId=1033,Izakaya,425
amenityId=1034,Seafood Restaurant,199
amenityId=1035,Skewer,51
amenityId=1080,Cooked Food Center,243
amenityId=1081,Crab Specialty,23
amenityId=1083,Food Wise Eateries,1070
amenityId=1084,Food Truck,12
amenityId=1091,Family Friendly,73
amenityId=1092,Vending Machine,40
amenityId=1093,Salt & Sugar Reduction Restaurant,1272
amenityId=1094,Cake Shop,262
amenityId=20228,Online Shop/ Food Distributor,609
amenityId=20229,Theme Restaurant,105
amenityId=20230,Sweets,289
amenityId=20231,Celebrity Shop,74
amenityId=20232,Pet Friendly,213
amenityId=20233,Nostalgic,146
amenityId=20236,No Shark Fin,113
'''.strip('\n').split('\n')],columns=['searchKey','name','count'])

dishes_df = pd.DataFrame.from_records([s.split(',') for s in 
'''
dishId=1001,Hot Pot,1009
dishId=1003,Bakery,1978
dishId=1004,Food Stall Noodles,484
dishId=1005,Ramen,499
dishId=1006,Taiwanese Drink,973
dishId=1008,Wine,973
dishId=1009,Seafood,1170
dishId=1010,Noodles/Rice Noodles,2780
dishId=1011,Vegetarian,459
dishId=1013,Herbal Tea,430
dishId=1014,Dessert,1263
dishId=1015,Ice Cream/yogurt,367
dishId=1016,Fine Dried Seafood,102
dishId=1017,Soup,231
dishId=1018,Congee,415
dishId=1019,BBQ,347
dishId=1020,Chinese BBQ,678
dishId=1022,Pizza,743
dishId=1024,Teppanyaki,148
dishId=1025,Roast Meat,335
dishId=1026,Sandwich,541
dishId=1028,Robatayaki,82
dishId=1030,Shanghai Hairy Crab,105
dishId=1031,Herbal Cuisine,185
dishId=1032,Buffet,239
dishId=1033,Curry,510
dishId=1034,Sushi/Sashimi,1402
dishId=1035,Hamburger,722
dishId=1036,Dim Sum,1296
dishId=1037,Udon,247
dishId=1039,Wonton/Dumpling,687
dishId=1040,Hot Chili Oil,13
dishId=1041,Chinese Buns,408
dishId=1071,Certified Halal Food,54
dishId=1072,Skewer,930
dishId=1073,Meatless Menu,383
dishId=1074,Chicken Hot Pot,341
dishId=1075,All Day Breakfast,498
dishId=1076,All-you-can-eat,144
dishId=1079,Chinese Cake,252
dishId=1080,Juice,296
dishId=1081,Salad,681
dishId=1082,Big Bowl Feast,60
dishId=1083,Organic Food,80
dishId=1084,Snake Soup,27
dishId=1085,Korean Fried Chicken,153
dishId=1086,Korean BBQ,99
dishId=1200,Fine Dining,100
dishId=1201,Kaiseki,13
dishId=1202,Sweet Soup,197
dishId=1203,Cake,1434
dishId=1204,Steam Hotpot,32
dishId=1205,Omakase,198
dishId=1206,Chinese New Year Products,97
dishId=1302,Brunch,119
'''.strip('\n').split('\n')],columns=['searchKey','name','count'])