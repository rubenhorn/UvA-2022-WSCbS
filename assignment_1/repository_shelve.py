from msilib.schema import Error
from pathlib import Path
import shelve

db_path = (Path(__file__).parent / 'data').absolute()

def _open_db():
    return shelve.open(str(db_path))

def put_url(key, url):
    with _open_db() as db:
        db[key] = url

def get_url(key):
    with _open_db() as db:
        return db.get(key, None)

def delete_url(key):
    with _open_db() as db:
        del db[key]

def has_url(key):
    with _open_db() as db:
        return key in db

def scan_keys(filter_func):
    with _open_db() as db:
        return [key for key in db if filter_func(key)]
