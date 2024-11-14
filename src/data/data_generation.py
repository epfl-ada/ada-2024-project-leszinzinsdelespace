from tqdm import tqdm
import src.data.data_loader as data_loader
from src.utils.utils import cosine_similarity
import pandas as pd
from openai import OpenAI
from src.utils.constants import OPENAI_API_KEY

def get_embedding(article):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(input=article, model="text-embedding-3-large").data[0].embedding
    return response

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
        all_path_similarities.append({'path': path, 'similarities': similarities, 'target': row['target']})
        
    pd.DataFrame(all_path_similarities).to_csv(output_file,index=False)