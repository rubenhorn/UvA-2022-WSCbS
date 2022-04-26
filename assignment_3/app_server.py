from http.client import BAD_REQUEST, CREATED, FORBIDDEN, NO_CONTENT, NOT_FOUND, OK, UNAUTHORIZED
from flask import Flask, request
from flask_cors import CORS
import utils
import werkzeug.exceptions

app = Flask(__name__)
CORS(app)

DB_NAME = 'url_service'
COLLECTION_NAME = 'mappings'

def put_url_and_user(key, url, user):
    mappings = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    doc = None
    try:
        doc = mappings[key]
    except:
        pass
    if doc is None:
        doc = mappings.createDocument()
    doc._key = key
    doc['value'] = (url, user)
    doc.save()

def get_url_and_user(key):
    mappings = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    try:
        return mappings[key]['value']
    except:
        return None

def delete_url_and_user(key):
    mappings = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    try:
        return mappings[key].delete()
    except:
        pass

def has_url(key):
    return get_url_and_user(key) is not None

def scan(filter_func):
    mappings = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    return [kv._key for kv in mappings.fetchAll() if filter_func(kv._key, kv['value'])]

# ==================== PARTIAL ROUTES ====================

def get_url(key):
    if has_url(key):
        url = get_url_and_user(key)[0]
        return utils.get_redirect_response(url)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def update_url(user, key, new_url):
    if not utils.is_url_valid(new_url):
        return utils.get_error_response(BAD_REQUEST, 'Invalid URL')
    if has_url(key):
        if get_url_and_user(key)[1] != user:
            return utils.get_error_response(FORBIDDEN, 'Forbidden')
        put_url_and_user(key, new_url, user)
        return utils.get_data_response(OK, None)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def delete_url(user, key):
    if has_url(key):
        if get_url_and_user(key)[1] != user:
            return utils.get_error_response(FORBIDDEN, 'Forbidden')
        delete_url_and_user(key)
        return utils.get_data_response(NO_CONTENT, None)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def get_keys(user):
    keys = scan(lambda _, value: value[1] == user)
    keys_and_urls = [{ 'key': key, 'url': str(get_url_and_user(key)[0]) } for key in keys]
    return utils.get_data_response(OK, { 'shortened_urls': keys_and_urls })

def create_url(user, url):
    if not utils.is_url_valid(url):
        return utils.get_error_response(BAD_REQUEST, 'Invalid URL')
    key = utils.create_unique_id()
    put_url_and_user(key, url, user)
    return utils.get_data_response(CREATED, { 'id': key })

# ==================== ROUTES ====================

@app.route('/<key>', methods=['GET', 'PUT', 'DELETE'])
def route_url(key):
    user = utils.get_user(request)
    if request.method != 'GET' and user is None:
        res = utils.get_error_response(FORBIDDEN, 'Forbidden')
    else:
        if request.method == 'GET':
            res = get_url(key)
        elif request.method ==  'PUT':
            url = utils.url_from_request(request)
            res = update_url(user, key, url)
        elif request.method ==  'DELETE':
            res = delete_url(user, key)
        else:
            raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def route_keys():
    user = utils.get_user(request)
    if user is None:
        res = utils.get_error_response(FORBIDDEN, 'Forbidden')
    else:
        if request.method ==  'GET':
            res = get_keys(user)
        elif request.method ==  'POST':
            url = utils.url_from_request(request)
            res = create_url(user, url)
        elif request.method ==  'DELETE':
            res = utils.get_error_response(NOT_FOUND, 'Nothing to delete')
        else:
            raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res
