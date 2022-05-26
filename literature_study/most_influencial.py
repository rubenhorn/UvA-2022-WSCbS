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

# For each topic
for topic, group in grouped_by_topic:
    # Skip non primary topics
    if not group['is_primary'].iloc[0]:
        continue
    print('\n', topic)
    # Get the n most cited papers
    most_cited = group.sort_values('citation_count', ascending=False).head(5)
    for item in most_cited.itertuples():
        get_paper_url(item.paper_id)
print('\nDone')
