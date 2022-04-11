_data = dict()

def put_url_and_user(key, url, user):
    global _data
    _data[key] = (url, user)

def get_url_and_user(key):
    global _data
    return _data.get(key)

def delete_url(key):
    global _data
    del _data[key]

def has_url(key):
    global _data
    return key in _data

def scan(filter_func):
    global _data
    return [key for key in _data if filter_func(key, _data[key])]
