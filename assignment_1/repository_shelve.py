from pathlib import Path
import shelve

def _open_db():
    filename = str((Path(__file__).parent / 'data').absolute())
    return shelve.open(filename)

def put_url(key, url):
    with _open_db() as db:
        db[key] = url

def get_url(key):
    with _open_db() as db:
        return db[key]

def delete_url(key):
    with _open_db() as db:
        del db[key]

def has_url(key):
    with _open_db() as db:
        return key in db

def scan_keys(filter_func):
    with _open_db() as db:
        return [key for key in db if filter_func(key)]
