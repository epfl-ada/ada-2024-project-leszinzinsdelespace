import urllib.parse

def url_decode(url_encoded):
    return urllib.parse.unquote(url_encoded).replace('_', ' ')

def path_to_list(path):
    return path.split(';')
