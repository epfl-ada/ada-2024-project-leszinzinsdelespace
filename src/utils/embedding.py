from src.data.data_loader import get_embeddings

embeddings = get_embeddings()
def get_embedding(article):
    return embeddings[embeddings['article'] == article].iloc[0]['embedding']