import requests
import pandas as pd
from requests.compat import urljoin

base = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/'
headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}


#Customize Date Here
year = 2015
month = 10
date = str(year) + "/" + str(month)

arts = []
for day in range (1, 31):
    curr_day = str(day).zfill(2)
    curr_day = date + "/" +  curr_day
    api_url = urljoin(base, curr_day)
    print(api_url) 
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        data = response.json()
    arts = data['items'][0]['articles']
    if day == 1:
        df = pd.DataFrame(arts)
        original = pd.DataFrame(arts)
    else:
        new_df = pd.DataFrame(arts)       
        df = pd.concat([df, new_df], ignore_index=True, axis=0)
        original = pd.concat([original, new_df], ignore_index=True, axis=0)
    df = df.groupby('article', as_index=False)['views'].sum()
    df = df.sort_values('views', ascending=False)
print("The Most Viewed articles are listed in descending order below:")
print(df)
print ("############################################################")
article_name = input("To check a specific view count of an article, Enter the article name: ")
print ("############################################################")
view_counts = df.loc[df['article'] == article_name, 'views'].values
max_view_counts = original.groupby('article')['views'].max()
day_max_view = original.loc[original['article'] == article_name, 'views'].values
s = pd.Series(day_max_view)
max_day = s.idxmax()
if len(view_counts) > 0:
    print("View counts for article", article_name + ":", view_counts[0])
    print("Day with most viewed: ", year, "/", month, "/", max_day)
    print("Most viewed day count: ", day_max_view[max_day])
else:
    print("Article not found")


