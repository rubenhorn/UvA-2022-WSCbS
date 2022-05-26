#! /usr/bin/python3


import pandas as pd
from pathlib import Path
import requests

# Load papers
df = pd.read_csv(Path(__file__).parent / 'papers.csv')

# Group by topic
grouped_by_topic = df.groupby('search_term')

def get_paper_url(paper_id):
    api_url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,url'
    resp = requests.get(api_url)
    json_resp = resp.json()
    print('   -', json_resp['title'])
    print('    ', json_resp['url'])

# All papers where the topic is idaas
idaas = df[df['search_term'] == 'idaas']

# Intersection with decentralized identity management
idaas_and_decentralized = idaas[idaas['paper_id'].isin(df[df['search_term'] == 'decentralized identity management']['paper_id'])]
# Sort by citation count
idaas_and_decentralized = idaas_and_decentralized.sort_values('citation_count', ascending=False)
print('\nIDaaS and decentralized identity management')
for item in idaas_and_decentralized.itertuples():
    get_paper_url(item.paper_id)
    print(f'     Citations:', item.citation_count)

# Intersection with federated identity management
idaas_and_federated = idaas[idaas['paper_id'].isin(df[df['search_term'] == 'federated identity management']['paper_id'])]
# Sort by citation count
idaas_and_federated = idaas_and_federated.sort_values('citation_count', ascending=False)
print('\nIDaaS and federated identity management')
for item in idaas_and_federated.itertuples():
    get_paper_url(item.paper_id)
    print(f'     Citations:', item.citation_count)

print('Done')
