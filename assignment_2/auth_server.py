import atexit
from http.client import BAD_REQUEST, FORBIDDEN, OK
from pathlib import Path
import shelve
from flask import Flask, request
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)

db_path = (Path(__file__).parent / 'users').absolute()
_db = None

def _open_db_if_closed():
    global _db
    if _db is None:
        if utils.get_config(app, 'EPHEMERAL'):
            _db = dict()
        else:
            _db = shelve.open(str(db_path))

def _close_db_if_open():
    global _db
    if _db is not None and not utils.get_config(app, 'EPHEMERAL'):
        _db.close()
    _db = None

atexit.register(_close_db_if_open)

def store_credentials_in_db(credentials):
    _open_db_if_closed()
    _db[credentials[0]] = credentials[1]
    try:
        _db.sync()
    except: # Ephemeral db can't be synced
        pass

def get_password_hash_from_db(username):
    _open_db_if_closed()
    return _db.get(username)

# ==================== ROUTES ====================

@app.route('/users', methods=['POST'])
def register():
    credentials = utils.get_credentials_from_request(request)
    if credentials is None:
        return utils.get_error_response(BAD_REQUEST, 'Invalid request body')
    if get_password_hash_from_db(credentials[0]) is not None:
        return utils.get_error_response(BAD_REQUEST, 'User already exists')
    store_credentials_in_db(credentials)
    return utils.get_data_response(OK, None)


@app.route('/users/login', methods=['POST'])
def login():
    credentials = utils.get_credentials_from_request(request)
    try:
        hash_db = get_password_hash_from_db(credentials[0])
        if hash_db != credentials[1]:
            raise Exception
    except:
        return utils.get_error_response(FORBIDDEN, 'Invalid credentials')
    return utils.get_data_response(OK, { 'bearer_token': utils.generate_token(credentials[0])})
