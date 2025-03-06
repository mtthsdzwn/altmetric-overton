import requests
import pandas as pd
import ast

def url_reader(my_url):
    global overton_data
    response = requests.get(my_url)
    for item in response.json()['results']['results']:
        # print(result)
        # item = ast.literal_eval(result)
        doi = item['document_url']
        title = item['title']
        docs = item['cited_by_documents']
        overton_data = pd.concat([overton_data, pd.DataFrame({'doi':doi, 'title':title, 'docs': docs})], ignore_index=True, axis=0)
    return response.json()['query']['next_page_url']


url = "https://app.overton.io/articles.php?identifiers=set%3A17121%3A91fab73070554c4b19f855d5f54085d3&sort=date&format=json&api_key=a49a2c-377135-1e2531"
overton_data = pd.DataFrame(columns=['doi', 'title', 'docs'])

while url :
    url = url_reader(url)
overton_data.to_csv('overton_data.csv', index=False)