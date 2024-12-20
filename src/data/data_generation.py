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
    G = nx.DiGraph()
    for _, row in links_df.iterrows():
    G.add_edge(row['linkSource'], row['linkTarget'])

    # Find strongly connected components
    strongly_connected = list(nx.strongly_connected_components(G))

    # Find the largest component
    largest_component = max(range(len(strongly_connected)), key=lambda x: len(strongly_connected[x]))
    largest_component_words = set(strongly_connected[largest_component])

    all_words_df = pd.read_csv('data/all_words_df.csv')
    articles = data_loader.load_articles()

    article_similarities = pd.read_csv('data/article_similarities_matrix.csv')
    article_similarities.columns = articles['article']
    article_similarities.index = articles['article']
    # Ensure that the DataFrame has rows and columns aligned by article
    article_similarities = article_similarities.loc[all_words_df['article'], all_words_df['article']]
    links = []

    # Precompute article indices
    article_indices = {article: idx for idx, article in enumerate(all_words_df['article'])}


    # Continue until no active points remain
    while len(largest_component_words) < len(all_words_df):
        similarities = []
        # Get articles not in largest component
        non_component_articles = set(all_words_df['article']) - largest_component_words
        
        # Iterate over articles not in largest component
        for article in tqdm(non_component_articles, desc="Processing active points"):
            article_idx = article_indices[article]
            similarity_row = article_similarities.iloc[article_idx]
            
            # Get similarities to articles in largest component
            component_similarities = {
                comp_article: similarity_row[comp_article] 
                for comp_article in largest_component_words
            }
            
            if component_similarities:
                # Find most similar article in component
                nearest_neighbor = max(component_similarities.items(), key=lambda x: x[1])
                similarities.append((nearest_neighbor[1], article, nearest_neighbor[0]))

        # Get closest pair
        sorted_similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
        closest_pair = sorted_similarities[0]

        # Add the chosen link
        source_article = closest_pair[1]  # Article outside component
        target_article = closest_pair[2]  # Article in component
        similarity = closest_pair[0]

        # Precompute descendants for target_article and source_article
        if source_article in G.nodes():
            source_descendants = nx.descendants(G, source_article)
            target_descendants = nx.descendants(G, target_article)

            if target_article in source_descendants:
                # Add edge only if source is a descendant of target
                G.add_edge(target_article, source_article)
                links.append((target_article, source_article, similarity))
                print(f"Added edge between {target_article} and {source_article}")
            elif source_article in target_descendants:
                # Add edge only if target is a descendant of source
                G.add_edge(source_article, target_article)
                links.append((source_article, target_article, similarity))
                print(f"Added edge between {source_article} and {target_article}")
        else:
            # If nodes are not connected or descendants cannot be determined
            G.add_edges_from([(source_article, target_article), (target_article, source_article)])
            links.extend([
                (source_article, target_article, similarity),
                (target_article, source_article, similarity)
            ])
            print(f"Added edge between {source_article} and {target_article}")
    strongly_connected = list(nx.strongly_connected_components(G))
    largest_component = max(range(len(strongly_connected)), key=lambda x: len(strongly_connected[x]))
    largest_component_words = set(strongly_connected[largest_component])

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

def get_should_link_dict(links, article_similarities,threshold=0):
    results = []
    for article in tqdm(articles['article']):
        article_links = links[links['linkSource'] == article]
        not_linked_articles = articles[~articles['article'].isin(article_links['linkTarget'])]
        not_linked_articles = not_linked_articles[not_linked_articles['article'] != article]  # Remove current article
        for target in not_linked_articles['article']:
            similarity = article_similarities.loc[article,target]
            if similarity > threshold:
                results.append((article,target,similarity))

    should_link_dict = {}
    for article, target,similarity in results:
        should_link_dict[article]= should_link_dict.get(article,[])+[target]
    return should_link_dict


def missing_links_but_present(links, article_similarities,threshold=0.5,output_file="missing_links_but_present.csv"): 
    should_link_dict = get_should_link_dict(links, article_similarities,)
    results = []
    for article in should_link_dict:
        content = open(f"data/plaintext_articles/{urllib.parse.quote(article.replace(' ', '_'))}.txt","r").read()
        content_lowered = content.lower()
        for target in should_link_dict[article]:
            target_lowered = target.lower()
            if target_lowered in content_lowered:
                print(f"{target} present in {article} but not linked")
                results.append((article,target))
    pd.DataFrame(results).to_csv(output_file,index=False)

def all_missing_links(links, article_similarities,output_file="all_missing_links.csv"):
    missing_links_but_present(links, article_similarities,threshold=0,output_file=output_file)
