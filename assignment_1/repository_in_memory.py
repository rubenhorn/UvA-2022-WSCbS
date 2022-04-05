_data = dict()

def put_url(key, url):
    global _data
    _data[key] = url

def get_url(key):
    global _data
    return _data.get(key)

def delete_url(key):
    global _data
    del _data[key]

def has_url(key):
    global _data
    return key in _data

def scan_keys(filter_func):
    global _data
    return [key for key in _data if filter_func(key)]
