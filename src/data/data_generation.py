from tqdm import tqdm
import src.data.data_loader as data_loader
from src.utils.similarity import cosine_similarity
import pandas as pd
from openai import OpenAI
from src.utils.constants import OPENAI_API_KEY
from src.utils.embedding import get_embedding
import networkx as nx
import numpy as np
import urllib.parse

def generate_embeddings():
    articles = data_loader.load_articles()
    embeddings = []
    for article in tqdm(articles['article']):
        embeddings.append({'article': article, 'embedding': get_embedding(article)})
    pd.DataFrame(embeddings).to_csv('data/embeddings.csv',index=False)


def generate_all_path_similarities(output_file='data/path_similarities.csv'):
    all_paths, _, _ = data_loader.load_paths()
    all_path_similarities = []
    for index, row in tqdm(all_paths.iterrows(),total=len(all_paths)):
        similarities = []
        path = row['traversed']
        for i in range(len(path)):
            similarity = cosine_similarity(get_embedding(path[i]),get_embedding(row['target']))
            similarities.append(round(float(similarity),3))
        all_path_similarities.append({'path': path, 'similarities': similarities, 'target': row['target'],'status': row['status']})
        
    pd.DataFrame(all_path_similarities).to_csv(output_file,index=False)

def generate_chosen_links():
    pass

def generate_all_words_df():
    embeddings = pd.read_csv('data/embeddings.csv')
    articles = data_loader.load_articles()
    # Step 1: Flatten all articles into a single list
    all_words = articles['article']
    all_articles = set(all_words)
    word_counts = pd.Series(all_words).value_counts()
    all_words_df = pd.DataFrame({
        'article': list(word_counts.keys())
    })
    embedding_dict = dict(zip(embedding['article'], embedding['embedding']))
    all_words_df['embedding'] = all_words_df['article'].map(embedding_dict)
    all_words_df.to_csv('data/all_words_df.csv',index=False)

def generate_closest_neighbors():

    links_df = data_loader.load_links()
    G= nx.DiGraph()
    for _, row in links_df.iterrows():
        G.add_edge(row['linkSource'], row['linkTarget'])

        # Find strongly connected components
    strongly_connected = list(nx.strongly_connected_components(G))

    # Find the largest component
    largest_component = max(range(len(strongly_connected)), key=lambda x: len(strongly_connected[x]))
    largest_component_words = set(strongly_connected[largest_component])
    mask = np.array([word not in largest_component_words for word in all_words_df['article']])
    # Ensure mask is a boolean array
    mask = mask.astype(bool)
    all_words_df = pd.read_csv('data/all_words_df.csv')

    article_similarities = pd.read_csv('data/article_similarities_matrix.csv')
    article_similarities.columns = articles['article']
    article_similarities.index = articles['article']
    # Ensure that the DataFrame has rows and columns aligned by article
    article_similarities = article_similarities.loc[all_words_df['article'], all_words_df['article']]
    links = []

    # Continue until no active points remain
    while mask.any():
        similarities = []
        active_points = np.where(mask)[0]

        # Iterate over each active point
        for point in tqdm(active_points, desc="Processing active points"):
            # Get similarity row for this point
            similarity_row = article_similarities.iloc[point]

            sorted_indices = np.argsort(-similarity_row.values)

            # Filter out active indices (we only want neighbors that are not in the mask)
            valid_indices = sorted_indices[~mask[sorted_indices]]

            # Take the nearest valid neighbor
            nearest_index = valid_indices[0]
            nearest_neighbor = all_words_df.iloc[nearest_index]['article']

            # Store tuple: (similarity, source_index, target_article)
            similarities.append((similarity_row.iloc[nearest_index], point, nearest_neighbor))

        # If no similarities found for any active point, break out to avoid infinite loop
        if len(similarities) == 0:
            break

        # Sort by similarity in descending order and select the highest similarity pair
        sorted_similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
        closest_pair = sorted_similarities[0]

        # Add the chosen link
        source_article = all_words_df.iloc[closest_pair[1]]['article']
        target_article = closest_pair[2]
        similarity = closest_pair[0]
        links.append((source_article, target_article, similarity))

        # Deactivate the chosen source point
        mask[closest_pair[1]] = False

    closest_neighbors_df = pd.DataFrame(links, columns=['source_article', 'target_article', 'similarity'])
    closest_neighbors_df.to_csv('data/closest_neighbors.csv',index=False)

def generate_analysis_links():
    analysis_results = []

    for i, row in links_df.iterrows():
        source = row['source_article']
        target = row['target_article']
        source_file = f"data/plaintext_articles/{urllib.parse.quote(source.replace(' ', '_'))}.txt"
        target_file = f"data/plaintext_articles/{urllib.parse.quote(target.replace(' ', '_'))}.txt"

        # Read and preprocess
        full_source = open(source_file, "r").read().lower()
        full_target = open(target_file, "r").read().lower()
        
        reverse_link = (source.lower() in full_target)
        forward_link = (target.lower() in full_source)

        # Determine relationship type
        if forward_link and reverse_link:
            relationship = "both"
        elif forward_link and not reverse_link:
            relationship = "forward_only"
        elif not forward_link and reverse_link:
            relationship = "reverse_only"
        else:
            relationship = "none"

        analysis_results.append({
            "source_article": source,
            "target_article": target,
            "forward_link_exists": forward_link,
            "reverse_link_exists": reverse_link,
            "relationship": relationship
        })
    analysis_df = pd.DataFrame(analysis_results)
    analysis_df['semantic_distance'] = analysis_df.apply(lambda row: article_similarities.loc[row['source_article'], row['target_article']], axis=1)
    analysis_df.to_csv('data/analysis_df.csv',index=False)

def wayanalysis():
    links = data_loader.load_links()
    article_similarities = pd.read_csv('data/article_similarities_matrix.csv')
    G = nx.DiGraph()
    for _, row in links.iterrows():
        G.add_edge(row['linkSource'], row['linkTarget'])
    # Get one-way and two-way edges
    one_way_edges = []
    two_way_edges = []

    for u, v in G.edges():
        # Check if the reverse edge exists
        if G.has_edge(v, u):
            # This edge pair is bidirectional
            two_way_edges.append((u, v))
        else:
            # This edge is only one-way
            one_way_edges.append((u, v))

    # Calculate semantic distances for both types of edges
    one_way_distances = []
    two_way_distances = []

    for u, v in one_way_edges:
        # Get indices for the distance matrix
        u_idx = articles[articles['article'] == u].index[0]
        v_idx = articles[articles['article'] == v].index[0]
        one_way_distances.append(article_similarities.iloc[u_idx, v_idx])


    for u, v in two_way_edges:
        u_idx = articles[articles['article'] == u].index[0]
        v_idx = articles[articles['article'] == v].index[0]
        two_way_distances.append(article_similarities.iloc[u_idx, v_idx])
    one_way_distances_df = pd.DataFrame(one_way_distances, columns=['one_way_distance'])
    two_way_distances_df = pd.DataFrame(two_way_distances, columns=['two_way_distance'])
    one_way_distances_df.to_csv('data/one_way_distances_df.csv',index=False)
    two_way_distances_df.to_csv('data/two_way_distances_df.csv',index=False)

def missing_links_but_present(links, article_similarities): #TODO ALBERT
    pass

def missing_links_but_present_all_complete_full_integral(links, article_similarities): #TODO ALBERT
    pass