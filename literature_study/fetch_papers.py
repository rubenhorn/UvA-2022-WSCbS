#! /usr/bin/python3

from pathlib import Path
import sys
import pandas as pd
import requests
import random

search_terms = [
    { 'term': 'idaas', 'is_primary': True },
    # { 'term': 'identity as a service','is_primary': True },
    { 'term': 'federated identity management', 'is_primary': True },
    { 'term': 'decentralized identity management', 'is_primary': True },
    { 'term': 'self-sovereign identity', 'is_primary': True },
    { 'term': 'identity and access management', 'is_primary': True },
    { 'term': 'identity management', 'is_primary': True },
]

checkpoint = Path(__file__).parent / 'checkpoint.txt'
checkpoin_set = False
def set_checkpoint(term, offset):
    global checkpoin_set
    checkpoint.write_text(term + ':' + str(offset))
    checkpoin_set = True

# Load checkpoint
checkpoint_term = None
checkpoint_offset = -1
if checkpoint.exists():
    checkpoint_str = checkpoint.read_text()
    checkpoint_str = checkpoint_str.split(':')
    checkpoint_term = checkpoint_str[0]
    checkpoint_offset = int(checkpoint_str[1])
    # Delete checkpoint
    checkpoint.unlink()

def get_json_resp(resp):
    json_resp = None
    if resp.status_code == 429:
        print('Too many requests!', file=sys.stderr)
        raise Exception('Too many requests!')
    if resp.status_code == 200:
        json_resp = resp.json()
    else:
        print(f'Error {resp.status_code}', file=sys.stderr)
        print(resp.text, file=sys.stderr)
    return json_resp


def search_papers(search_term):
    global checkpoint_offset
    api_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = dict()
    params['query'] = search_term
    params['fields'] = ','.join(['paperId', 'year', 'citationCount'])
    params['offset'] = 0 if checkpoint_offset == -1 else checkpoint_offset
    checkpoint_offset = 0 # reset
    params['limit'] = 100
    json_resp = get_json_resp(requests.get(api_url, params=params))
    total = json_resp['total']
    print(total)
    papers = json_resp['data']
    # print('   offset =',params['offset'], 'limit =', params['limit'], 'got', len(json_resp['data']))
    while json_resp is not None and 'next' in json_resp and json_resp['next'] > 0:
        params['offset'] += params['limit']
        try:
            json_resp = get_json_resp(requests.get(api_url, params=params))
        except Exception as e:
            set_checkpoint(search_term, params['offset'])
            break
        if json_resp is not None:
            # print('   offset =',params['offset'], 'limit =', params['limit'], 'got', len(json_resp['data']))
            papers.extend(json_resp['data'])
    # remove duplicate papers
    papers_deduplicated = dict()
    for paper in papers:
        papers_deduplicated[paper['paperId']] = paper
    papers = list(papers_deduplicated.values())
    assert len(papers) == total, f'Expeted {total} papers, got {len(papers)}'
    return papers


search_term = []
is_primary = []
paper_id = []
year = []
citation_count = []

for item in search_terms:
    term = item['term']
    if checkpoint_term is not None and checkpoint_term != term:
        continue
    checkpoint_term = None # reset
    print(term, end='...')
    papers = search_papers(term)
    for paper in papers:
        search_term.append(term)
        is_primary.append(item['is_primary'])
        paper_id.append(paper['paperId'])
        year.append(paper['year'])
        citation_count.append(paper['citationCount'])
    if checkpoin_set:
        break

# DataFrame with columns search term, is primary, paperId, year, citation count
df = pd.DataFrame({
    'search_term': search_term,
    'is_primary': is_primary,
    'paper_id': paper_id,
    'year': year,
    'citation_count': citation_count
})
df['year'] = df['year'].fillna(-1)
df['year'] = df['year'].astype(int)


out_path = str(Path(__file__).parent / 'papers.csv')

# Load existing data frame if it exists
if Path(out_path).exists():
    df_checkpoint = pd.read_csv(out_path, index_col=0)
    df = df.append(df_checkpoint)

# Remove duplicate rows (search term + paper id)
df.drop_duplicates(subset=['search_term', 'paper_id'], inplace=True)

# Export CSV
df.to_csv(out_path, index=False)

print('Done')
