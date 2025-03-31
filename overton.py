import requests
import pandas as pd
import ast

def url_reader(my_url):
    global overton_data
    global index_number
    response = requests.get(my_url)
    for item in response.json()['results']['results']:
        doi = item['document_url']
        title = item['title']
        docs = item['cited_by_documents']
        for doc in docs:
            index_number += 1
            policy_document_id = doc.get('policy_document_id')
            policy_source_id = doc.get('policy_source_id')
            source_title = doc.get('source_title')
            document_title = doc.get('document_title')
            published_on = doc.get('published_on')
            document_url = doc.get('document_url')
            doc_type = doc.get('type')
            subtype = doc.get('subtype')
            country = doc.get('country')
            topics = doc.get('topics')
            classifications = doc.get('classifications')
            doc_url = doc.get('url')

            temper = pd.Series({
                'index': index_number,
                'doi':doi,
                'title':title,
                'policy_document_id': policy_document_id,
                'policy_source_id': policy_source_id,
                'source_title': source_title,
                'document_title': document_title,
                'published_on': published_on,
                'document_url': document_url,
                'type': doc_type,
                'subtype': subtype,
                'country': country,
                # 'topics': topics,
                # 'classifications': classifications,
                'url': doc_url
                },
            )
            overton_data = pd.concat([overton_data, temper.to_frame().T], ignore_index=True, axis=0)
    return response.json()['query']['next_page_url']


'''
initialize the variables
'''

pages_of_overton_data = ""
overton_data = pd.DataFrame(columns=['index','doi', 'title', 'policy_document_id', 'policy_source_id', 'source_title', 'document_title',
                                        'published_on', 'document_url', 'type', 'subtype', 'country',
                                        # 'topics', 'classifications',
                                        'url']
                            )
index_number = 0
# print(overton_data)

'''
loop through the api
'''

while pages_of_overton_data :
    pages_of_overton_data = url_reader(pages_of_overton_data)

'''
sanity check and save
'''

print(overton_data)
overton_data.to_csv('./csvFiles/overton_data.csv', index=False)