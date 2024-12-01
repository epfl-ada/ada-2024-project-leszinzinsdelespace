import pandas as pd
import numpy as np
from src.utils.utils import url_decode,path_to_list

def load_paths():
    paths_finished = pd.read_csv('data/wikispeedia_paths-and-graph/paths_finished.tsv', sep='\t', comment='#', names=['hashedIpAddress', 'timestamp', 'durationInSec', 'path', 'rating'])
    paths_unfinished = pd.read_csv('data/wikispeedia_paths-and-graph/paths_unfinished.tsv', sep='\t', comment='#', names=['hashedIpAddress', 'timestamp', 'durationInSec', 'path', 'target', 'type'])
    paths_finished['status'] = 'finished'
    paths_unfinished['status'] = 'unfinished'
    paths_unfinished['target'] = paths_unfinished['target'].apply(url_decode)
    paths_finished['target'] = paths_finished['path'].apply(lambda x: url_decode(x.split(';')[-1]))
    paths_unfinished['durationInSec'] = paths_unfinished.apply(lambda row: row['durationInSec'] if not row['type'] == 'timeout' else row['durationInSec']-1800, axis=1)
    paths_finished['backtracks'] = paths_finished['path'].apply(find_backtracks)
    paths_unfinished['backtracks'] = paths_unfinished['path'].apply(find_backtracks)
    paths_finished['traversed'] = paths_finished['path'].apply(path_to_list)
    paths_unfinished['traversed'] = paths_unfinished['path'].apply(path_to_list)

    all_paths = pd.concat(
        [paths_finished,paths_unfinished],
        ignore_index=True,
        copy=True
    )
    
    return all_paths, paths_finished, paths_unfinished

def load_articles():
    articles = pd.read_csv('data/wikispeedia_paths-and-graph/articles.tsv', sep='\t', comment='#', names=['article'])
    articles['article'] = articles['article'].apply(url_decode)
    return articles

def load_categories():
    categories = pd.read_csv('data/wikispeedia_paths-and-graph/categories.tsv', sep='\t', comment='#', names=['article', 'category'])
    categories['article'] = categories['article'].apply(url_decode)
    return categories

def load_links():
    links = pd.read_csv('data/wikispeedia_paths-and-graph/links.tsv', sep='\t', comment='#', names=['linkSource', 'linkTarget'])
    links['linkSource'] = links['linkSource'].apply(url_decode)
    links['linkTarget'] = links['linkTarget'].apply(url_decode)
    return links

def load_chosen_links():
    chosen_links = pd.read_csv('data/chosen_links_rank.csv')
    return chosen_links

def load_distance_matrix():
    matrix = []
    with open("data/wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt", 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
            # Convert each character to integer, ignoring underscores
            row = [int(char.replace('_', '-1')) for char in line.strip()]
            matrix.append(row)
    
    return np.array(matrix)

def load_all_path_similarities():
    all_path_similarities = pd.read_csv('data/similarities.csv')
    all_path_similarities_unfinished = all_path_similarities[all_path_similarities['status'] == 'unfinished']
    all_path_similarities_finished = all_path_similarities[all_path_similarities['status'] == 'finished']
    return all_path_similarities_unfinished, all_path_similarities_finished

def get_embeddings():
    embeddings = pd.read_csv('data/embeddings.csv')
    embeddings['embedding'] = embeddings['embedding'].apply(lambda x: eval(x))
    embeddings['article'] = embeddings['article'].apply(url_decode)
    return embeddings

def find_backtracks(path):
    # Split the path into words
    words = path.split(';')
    stack = []
    backtracks = []

    for word in words:
        if word == "<":
            if stack:
                backtracks.append(stack.pop())  # Record the last valid word as a backtrack
        else:
            stack.append(url_decode(word))  # Decode and push the word onto the stack

    # Filter out empty or invalid entries before returning
    return [word for word in backtracks if word]

