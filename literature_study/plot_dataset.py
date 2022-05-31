#! /usr/bin/python3
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

out_dir = Path(__file__).parent
file_extension = '.pdf'

# load data
df = pd.read_csv(out_dir / 'papers.csv')
# Drop publications before 1980
year_min = 1980
year_max = 2022
df = df[df['year'] >= year_min]
df = df[df['year'] <= year_max]

grouped_by_term = df.groupby('search_term')


# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
# Iterate over groups
legend = []
markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd']
for i, (term, group) in enumerate(grouped_by_term):
    legend.append(term)
    # Compute value counts (year)
    counts = group['year'].value_counts()
    # Sort by index
    counts = counts.sort_index()
    # Plot counts
    ax.plot(counts.index, counts.values, label=term, marker=markers[i])
# Add legend
ax.legend(legend)
# Add title
ax.set_title('Publication frequency by year')
# Add x-axis label
ax.set_xlabel('Year')
# Add y-axis label
ax.set_ylabel('Number of publications')
# Show plot
plt.savefig(out_dir / f'papers_per_year{file_extension}')

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
# Iterate over groups
legend = []
for i, (term, group) in enumerate(grouped_by_term):
    legend.append(term)
    # Compute value counts (year)
    counts = group['year'].value_counts()
    # Sort by index
    counts = counts.sort_index()
    # Plot counts
    ax.plot(counts.index, counts.values / counts.sum(), label=term, marker=markers[i])
# Add legend
ax.legend(legend)
# Add title
ax.set_title('Publication frequency by year')
# Add x-axis label
ax.set_xlabel('Year')
# Add y-axis label
ax.set_ylabel('Fraction of total publications')
# Show plot
plt.savefig(out_dir / f'papers_per_year_relative{file_extension}')

# For each group
mean_pubs_per_years = []
std_pubs_per_years = []
mean_citation_counts = []
std_citation_counts = []
for term, group in grouped_by_term:
    # Mean publications per year
    mean_counts = group['year'].value_counts().mean()
    # Std publications per year
    std_counts = group['year'].value_counts().std()
    # Mean citation count
    mean_citation_count = group['citation_count'].mean()
    # Std citation count
    std_citation_count = group['citation_count'].std()
    # Append to list
    mean_pubs_per_years.append(mean_counts)
    std_pubs_per_years.append(std_counts)
    mean_citation_counts.append(mean_citation_count)
    std_citation_counts.append(std_citation_count)
stats = pd.DataFrame({
    'search_term': grouped_by_term.groups.keys(),
    'mean_pubs_per_years': mean_pubs_per_years,
    'std_pubs_per_years': std_pubs_per_years,
    'mean_citation_counts': mean_citation_counts,
    'std_citation_counts': std_citation_counts
})
# Round columns to 2 decimals
stats = stats.round(2)
stats.to_csv(out_dir / 'stats.csv', index=False)

# Count of papers per term as dictionary
counts = []
for term, group in grouped_by_term:
    counts.append(len(group))

# Compute matrix of overlap
overlap = np.zeros((len(counts), len(counts)))
# iterate over groups with index
for i, (term1, group1) in enumerate(grouped_by_term):
    for j, (term2, group2) in enumerate(grouped_by_term):
        # Count overlap
        overlap[i, j] = len(group1.merge(group2, on='paper_id', how='inner'))
        # Normalize by row
        overlap[i, j] /= counts[i]
# Convert overlap to dataframe
labels = grouped_by_term.groups.keys()
# 'decentralized identity management', 'federated identity management', 'idaas', 'identity and access management', 'identity management', 'self-sovereign identity'
labels = ['dim', 'fim', 'idaas', 'iam', 'im', 'ssi']
overlap = pd.DataFrame(overlap, index=labels, columns=labels)
# Plot matrix
fig, ax = plt.subplots(figsize=(5, 3))
# Title
ax.set_title('Overlap of publications normalized by row')
sns.heatmap(overlap, annot=True, cbar=False)
plt.yticks(rotation=0) 
plt.tight_layout()
plt.savefig(out_dir / f'overlap{file_extension}')

print('number of publications', len(df))
# print number of publications per term
for term, group in grouped_by_term:
    print(term, len(group), '({:.2f}%)'.format(100 * len(group) / len(df)))

print('\nDone')
