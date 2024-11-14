import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity as cosine_similarity_sklearn
from src.utils.embedding import get_embedding


def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_cosine_similarity_for_path_word_by_word(path, target_word, model):
    target_embedding = model.encode([target_word], device="mps")

    # Calculate cosine similarities for each word in the path
    similarities = []
    for word in path:
        word_embedding = model.encode([word], device="mps")
        cosine_score = cosine_similarity_sklearn(word_embedding, target_embedding).flatten()[0]
        similarities.append(float(cosine_score))
    return similarities

def get_cosine_similarity_for_path_word_by_word_openai(path, target_word):
    target_embedding = get_embedding(target_word)

    similarities = []
    for word in path:
        word_embedding = get_embedding(word)
        cosine_score = cosine_similarity(word_embedding, target_embedding)
        similarities.append(float(cosine_score))
    return similarities

def should_have_link(current,target,threshold=0.4):
    current_embedding = get_embedding(current)
    target_embedding = get_embedding(target)
    similarity = cosine_similarity(current_embedding,target_embedding)
    return bool(similarity >= threshold),float(similarity)