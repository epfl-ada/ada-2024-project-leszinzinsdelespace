import numpy as np
import pandas as pd
from src.utils.utils import url_decode
from src.data.data_loader import load_distance_matrix, load_articles

distance_matrix = load_distance_matrix()

articles_df = load_articles()



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