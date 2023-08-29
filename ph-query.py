import requests
import json
import pandas as pd
import textwrap

api_url = "https://api.producthunt.com/v2/api/graphql"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ad1Vh9aJoOSuPZ8EqNRIPMlk-qpTZalnNVpdwjIWcas',
    'Host':'api.producthunt.com',
}

columns = ['id','name','tagline','desc','website','category','thumbnail','votes','comments','createdAt','launchedAt']
data_frame = pd.DataFrame(columns=columns)

count = 0

def get_products(date):
  global count
  print(date,count)
  date = date.strftime("%d-%m-%Y")
  query = 'query{ posts(order: VOTES,postedAfter: "' + date + ' 00:00", postedBefore: "' + date +' 23:59"){ edges{ node{ thumbnail{ type url } id name tagline description website votesCount commentsCount topics{ nodes{ name } } featuredAt createdAt } } } }'
  response = requests.post(api_url, json={'query': query}, headers=headers)

  # Complete Long URL
  def get_long_url(short_url):
      response = requests.get(short_url,timeout=5)
      if response.history:
          long_url = response.url
          return long_url
      else:
          print("No redirect found.")
          return None


  if response.status_code == 200:
      req_data = response.json()
      for idx,node in enumerate(req_data['data']['posts']['edges']):
          
          n = node['node']  #1
          ph_id = n['id'] #2
          name = n['name'] #3
          tagline = n['tagline'] #4
          desc = n['description'] #5
          website = n['website'] #6
          topics = n['topics'] #6
          cat = ''
          for topic in topics['nodes']:
            cat += topic['name'] + ','
          cat = cat[:-1]
          thumbnail = n['thumbnail']['url'] #7
          vote_count = n['votesCount'] #8
          comments_count = n['commentsCount'] #9
          created_at = n['createdAt'] #10
          launched_at = n['featuredAt'] #11

          try:
            print(f'Working on long link for {ph_id} {count}')
            website = get_long_url(f'https://www.producthunt.com/r/p/{ph_id}')
            if website:
              from urllib.parse import urlparse

              full_url = website
              parsed_url = urlparse(full_url)

              base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
              website = base_url;

              record = [ph_id,name,tagline,desc,website,cat,thumbnail,vote_count,comments_count,created_at,launched_at]
              data_frame.loc[count] = record
              count = count + 1
            else:
              print(f'Website unavailble for ${name} ${ph_id}')
          except:
            print("ERROR ===========================>",name,ph_id)

  else:
      print('Error: PH Server')
      print('Error:', response.status_code)



# Iterate the days of month
import datetime
def iterate_month_days(year, month):
    start_date = datetime.date(year, month, 1)
    next_month = month + 1 if month < 12 else 1
    end_date = datetime.date(year if next_month != 1 else year + 1, next_month, 1)
    
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += datetime.timedelta(days=1)

# Metion the Date and year 
year = 2023
month = 2
for date in iterate_month_days(year, month):
  get_products(date)
  # break; # enable to for the first day of the month

data_frame.to_csv(f"data-FEB-2023.csv", index=False)
