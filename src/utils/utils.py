import urllib.parse
import numpy as np
def url_decode(url_encoded):
    return urllib.parse.unquote(url_encoded).replace('_', ' ')

def path_to_list(path,keep_backtracks=False):
    if not keep_backtracks:
        path = path.replace(';<','')
    return [url_decode(p) for p in path.split(';')]

def shorten_list_finished(entry,n=10):
    similarities = eval(entry['similarities'].replace(" ", ""))  # Convert string representation of list to actual list
    path = eval(entry['path']) # Convert string representation of list to actual list
    if len(similarities) > n:
        return similarities[-n:],path[-n:]
    return similarities,path

def shorten_list_unfinished(entry,n=9):
    similarities = eval(entry['similarities'].replace(" ", ""))  # Convert string representation of list to actual list
    path = eval(entry['path'])

    max_value = max(similarities)
    if max_value < 0.3:
        return [],[]
    max_index = similarities.index(max_value)
    similarities = similarities[:max_index + 1]  # Keep only values up to and including max
    path = path[:max_index + 1]
    if len(similarities) > n:
        return similarities[-n:],path[-n:]
    return similarities,path

def get_missing_links(entry):
    # Return a Series instead of a tuple
    return pd.Series({
        'biggest_similarity_article': entry['path'][-1],
        'target': entry['target']
    })
