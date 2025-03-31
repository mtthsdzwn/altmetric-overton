import requests
import pandas as pd
import json
url = "https://api.openalex.org/works"

page = 1
my_year = 2019
my_institute = 'i865915315'
field_id = 11
sample_size = 500

savable = pd.DataFrame(
    columns=['ids', 'doi', 'topics', 'display_name', 'publication_year', 'fwci' , 'type', 'cited_by_count',
             'cited_by_percentile', 'authorships', 'open_access', 'sustainable_development_goals', 'counts_by_year',
             'abstract_inverted_index']
)

while True:
    my_params = {
        'per-page': '100',
        'page': str(page),
        'seed': '456',
        'sample': str(sample_size),
        'select': 'id,ids,doi,topics,display_name,publication_year,fwci,type,cited_by_count,cited_by_percentile_year,'
                  'authorships,open_access,sustainable_development_goals,counts_by_year,abstract_inverted_index',
        'filter': f'publication_year:{str(my_year)},authorships.institutions.id:{my_institute},type:types/article'
            f',topics.field.id:{str(field_id)}',
    }
    response_data =  requests.get(url, params=my_params).json()

    page += 1
    count = response_data['meta']['count']
    # print(count)
    for item in response_data['results']:
        # print(item)
        line_item = pd.DataFrame(
            columns=['ids', 'doi', 'topics', 'display_name', 'publication_year', 'fwci', 'type', 'cited_by_count',
                     'cited_by_percentile', 'authorships', 'open_access', 'sustainable_development_goals',
                     'counts_by_year',
                     'abstract_inverted_index']
        )
        # line_item['id'] = item.get('id')
        line_item['ids'] = (item.get('ids'))
        print(item.get('ids'))
        print(line_item['ids'])
        line_item['doi'] = item.get('doi')
        line_item['topics'] = str(item.get('topics')[0]['field']['display_name'])
        line_item['display_name'] = item.get('display_name')
        line_item['publication_year'] = item.get('publication_year')
        line_item['fwci'] = item.get('fwci')
        line_item['type'] = item.get('type')
        line_item['cited_by_count'] = item.get('cited_by_count')
        line_item['cited_by_percentile_year'] = item.get('cited_by_percentile_year')
        line_item['authorships'] = str(item.get('authorships'))
        line_item['open_access'] = item.get('open_access')
        line_item['sustainable_development_goals'] = str(item.get('sustainable_development_goals'))
        # line_item['counts_by_year'] = item.get('counts_by_year')
        # line_item['abstract_inverted_index'] = item.get('abstract_inverted_index')
        # print("LINE ITEM")
        # print(line_item)
        savable = pd.concat([savable, line_item], ignore_index=True, axis=0)
        # print("hoe lang is savable", savable.head(5))
    if page * 100 > sample_size:
        page = 1
        field_id += 1
        if field_id > 36: break

savable.drop_duplicates(['doi'], inplace=True)
savable.to_csv('./csvFiles/openAlex_data.csv', index=False)

savable['doi'].to_csv('./csvFiles/doi.csv', index=False)
