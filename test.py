import requests
import pandas as pd

def get_long_url(short_url):
    response = requests.get(short_url)
    if response.history:
        long_url = response.url
        return long_url
    else:
        print("No redirect found.")
        return None


columns = ['id','Date', 'ProductName','Topic','Short Url','Logn Url']

data_out = pd.DataFrame(columns=columns)
# data_out.loc[0] = ["Akas",20]

data_out.to_csv('out.csv',index=False)


# df_out = pd.
df = pd.read_csv('2022.csv')
links = df['ShortUrl'].tolist()
rowIndex = 0


for i in range(0,10):
    short_link = links[i];
    long_link = get_long_url(short_link);

    if long_link:
        date = df.iloc[i]['Date']
        product_name = df.iloc[i]['ProductName']
        tag = df.iloc[i]['Topic']
        print('Short Ling:', short_link, 'Long Link:', long_link);
        data_out.loc[rowIndex] = [rowIndex,date,product_name,tag,short_link,long_link]
        rowIndex += 1


data_out.to_csv('out.csv',index=False)



