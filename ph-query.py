import requests
import json
import pandas as pd

api_url = "https://api.producthunt.com/v2/api/graphql"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ad1Vh9aJoOSuPZ8EqNRIPMlk-qpTZalnNVpdwjIWcas',
    'Host':'api.producthunt.com',
}
query = """
query{
  posts(order: VOTES,postedAfter: "01-08-2023", postedBefore: "02-08-2023"){
    edges{
      node{
        thumbnail{
          type
          url
        }
        
        id
        name
        tagline
        description
        website
        votesCount
        commentsCount
        topics{
          nodes{
            name
          }
        }
        
        featuredAt
        createdAt
      }
    }
  }
}
"""

response = requests.post(api_url, json={'query': query}, headers=headers)

columns = ['id','name','tagline','desc','website','category','thumbnail','votes','comments','createdAt','launchedAt']
data_frame = pd.DataFrame(columns=columns)
row_index = 0

def get_long_url(short_url):
    response = requests.get(short_url)
    if response.history:
        long_url = response.url
        return long_url
    else:
        print("No redirect found.")
        return None



if response.status_code == 200:
    req_data = response.json()
    for node in req_data['data']['posts']['edges']:
        
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
        lauched_at = n['featuredAt'] #11
        
        if get_long_url(website):
          print(f'Working on long link for ${name} ${id}')
          record = [ph_id,name,tagline,desc,website,cat,thumbnail,vote_count,comments_count,created_at,lauched_at]
          data_frame.loc[row_index] = record
          row_index += 1
        else:
          print(f'Website unavailble for ${name} ${ph_id}')
else:
    print('Error:', response.status_code)


date = "01-08-2023"
data_frame.to_csv(f"data-{date}.csv", index=False)