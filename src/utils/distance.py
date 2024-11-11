import numpy as np
import pandas as pd
import urllib.parse

def load_distance_matrix(filepath):
    # Read the file and create matrix
    matrix = []
    with open(filepath, 'r') as file:
        for line in file:
            # Skip comment lines and empty lines
            if line.startswith('#') or not line.strip():
                continue
            # Convert each character to integer, ignoring underscores
            row = [int(char.replace('_', '-1')) for char in line.strip()]
            matrix.append(row)
    
    return np.array(matrix)

filepath = "data/wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt"
distance_matrix = load_distance_matrix(filepath)

articles_df = pd.read_csv('data/wikispeedia_paths-and-graph/articles.tsv', sep='\t', comment='#', names=['page'])
articles_df['page'] = articles_df['page'].apply(lambda x: urllib.parse.unquote(x).replace('_', ' '))



def get_article_index(article, articles_df):
    try:
        return articles_df[articles_df['page'] == article].index[0]
    except:
        print(f"Article not found: {article}")
        return None

print(get_article_index("Áedán mac Gabráin", articles_df))
print(get_article_index("Zulu", articles_df))

def get_distance(start, target):
    index_start = get_article_index(start, articles_df)
    index_target = get_article_index(target, articles_df)
    if index_start is None or index_target is None:
        print(f"Article not found: {start} or {target}")
        return pd.NA
    #print(f"index_start: {index_start}, index_target: {index_target}")
    d = distance_matrix[index_start][index_target]
    if d == -1:
        #print(f"No path found between {start} and {target}")
        return pd.NA
    return d