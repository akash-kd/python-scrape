import requests
import json
import pandas as pd
import textwrap


api_url = "https://api.producthunt.com/v2/api/graphql"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer cK2uKc17j7euT7RI26oyMhIGNniiZCBYZ7cS-aazYkM',
    'Host':'api.producthunt.com',
}

columns = ['id','name','tagline','desc','website','category','thumbnail','votes','comments','createdAt','launchedAt']
data_frame = pd.DataFrame(columns=columns)

  # Complete Long URL
def get_long_url(short_url):
    response = requests.get(short_url,timeout=5)
    if response.history:
        long_url = response.url
        return long_url
    else:
        print("No redirect found.")
        return None

def make_request(ph_id):
    query = "query { post(id: " + (str)(ph_id) + " ) { thumbnail { type url } id name tagline description website url votesCount commentsCount topics { nodes { name } } featuredAt createdAt } }"
    response = requests.post(api_url, json={'query': query}, headers=headers)
    if response.status_code != 200:
        print(response)
    if response.status_code == 200 and response.json()['data']:
        if response.json()['data']['post']:
            return response.json()['data']['post']


def get_product(ph_id):
    n = make_request(ph_id)
    if not n:
        return None
    node_id = n['id'] #2
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

    print(f'Working on long link for {ph_id} {node_id}',end="")


    try:
        website = get_long_url(website)
        if website:
            from urllib.parse import urlparse

            full_url = website
            parsed_url = urlparse(full_url)

            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            website = base_url;

            record = [node_id,name,tagline,desc,website,cat,thumbnail,vote_count,comments_count,created_at,launched_at]
            return record
        else: 
            print(f' Website unavailble for ${name} ${ph_id}',end="")
    except:
        print(f' ERROR =============> {ph_id} {name}',end="")


from csv import writer
head_column = ['id','name','tagline','desc','website','category','thumbnail','votes','comments','createdAt','launchedAt']


# with open('ph-data.csv', 'a') as csv_object:
#     csv = writer(csv_object)
#     csv.writerow(head_column)
#     csv_object.close()

count = 0
import time
for ph_id in range(697,1001):
    record = get_product(ph_id);
    print(" ",count)
    count += 1
    if count > 50:
        count = 0
        print("BREAK ================>")
        time.sleep(900)
    if record:
        with open('ph-data.csv', 'a') as csv_object:
            csv = writer(csv_object)
            csv.writerow(record)
            csv_object.close()
            


    
