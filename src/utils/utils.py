import urllib.parse
import numpy as np
def url_decode(url_encoded):
    return urllib.parse.unquote(url_encoded).replace('_', ' ')

def path_to_list(path,keep_backtracks=False):
    if not keep_backtracks:
        path = path.replace('<;','')
    return [url_decode(p) for p in path.split(';')]

def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))