import atexit
from pathlib import Path
import shelve

db_path = (Path(__file__).parent / 'data').absolute()

_db = None

def _open_db_if_closed():
    global _db
    if _db is None:
        _db = shelve.open(str(db_path))

def _close_db_if_open():
    global _db
    if _db is not None:
        _db.close()
        _db = None

atexit.register(_close_db_if_open)

def put_url_and_user(key, url, user):
    _open_db_if_closed()
    _db[key] = (url, user)
    _db.sync()

def get_url_and_user(key):
    _open_db_if_closed()
    return _db.get(key)

def delete_url(key):
    _open_db_if_closed()
    del _db[key]
    _db.sync()

def has_url(key):
    _open_db_if_closed()
    return key in _db

def scan(filter_func):
    _open_db_if_closed()
    return [key for key in _db if filter_func(key, _db[key])]
