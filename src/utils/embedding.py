from src.data.data_loader import get_embeddings
from openai import OpenAI
from src.utils.constants import OPENAI_API_KEY

embeddings = get_embeddings()
def get_embedding(article):
    if article not in embeddings['article'].values:
        return get_embedding_openai(article)
    return embeddings[embeddings['article'] == article].iloc[0]['embedding']

def get_embedding_openai(article):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(input=article, model="text-embedding-3-large").data[0].embedding
    return response