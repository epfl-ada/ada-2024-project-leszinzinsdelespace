import numpy as np
import pandas as pd
from src.utils.utils import url_decode
from src.data.data_loader import load_distance_matrix, load_articles

distance_matrix = load_distance_matrix()

articles_df = load_articles()



def get_article_index(article, articles_df):
    try:
        return articles_df[articles_df['article'] == article].index[0]
    except:
        print(f"Article not found: {article}")
        return None

print(get_article_index("Áedán mac Gabráin", articles_df))
print(get_article_index("Zulu", articles_df))

def get_distance(start, target):
    index_start = get_article_index(start, articles_df)
    index_target = get_article_index(target, articles_df)
    if index_start is None or index_target is None:
        return pd.NA
    d = distance_matrix[index_start][index_target]
    if d == -1:
        return pd.NA
    return d