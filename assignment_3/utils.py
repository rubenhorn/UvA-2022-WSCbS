import hashlib
import os
import time
from flask import Response
import json
from pyArango.connection import *
import uuid
import jwt
import validators

def get_config_or_exit(key):
    config = os.getenv(key, None)
    if config is None:
        print('Configuration key not found in environment: ' + key)
        exit(1)
    return config

mimetype = 'application/json'
_app_secret = os.getenv('APP_SECRET', '') # Not strictly necessary -> fallback to empty string
_jwt_secret = get_config_or_exit('JWT_SECRET')
_arango_url = get_config_or_exit('ARANGO_URL')
_arango_user = get_config_or_exit('ARANGO_USER')
_arango_password = get_config_or_exit('ARANGO_PASSWORD')

def is_url_valid(url):
    if url is None:
        return False
    if not url.startswith('http://') and not url.startswith('https://'):
        return False
    return validators.url(url)

def create_unique_id():
    return uuid.uuid4().hex[:8]

def get_user(request, default=None):
    header_key = 'Authorization'
    header_value = request.headers.get(header_key)
    user = default
    if str(header_value).startswith('Bearer '):
        return get_user_from_token(header_value[7:])
    return user

def get_error_response(status_code, message):
    json_data = {'status': 'error', 'data': {'message': message}}
    return Response(json.dumps(json_data), status_code, mimetype=mimetype)

def get_data_response(status_code, data):
    json_data = {'status': 'success', 'data': data}
    return Response(json.dumps(json_data), status_code, mimetype=mimetype)

def get_redirect_response(url):
    response = get_data_response(301, {'url': url})
    response.headers.add_header('Location', url)
    return response

def url_from_request(request):
    try:
        return request.json['url']
    except Exception:
        return None

def get_credentials_from_request(request):
    try:
        username = request.json['username']
        password = request.json['password']
        m1 = hashlib.new('sha256')
        m1.update((username + _app_secret).encode('utf-8'))
        m2 = hashlib.new('sha256')
        m2.update((password + m1.hexdigest()).encode('utf-8'))
        digest = m2.hexdigest()
        return (username, digest)
    except:
        return None

def generate_token(username):
    payload = {
        'sub': username,
        'iat': int(time.time()),
    }
    return jwt.encode(payload, _jwt_secret, algorithm='HS256')

def get_user_from_token(token, max_age=3600):
    try:
        payload = jwt.decode(token, _jwt_secret, algorithms=['HS256'])
        if payload['iat'] + max_age < time.time():
            return None # Expired
    except:
        return None
    return payload['sub']

def get_database_collection(db_name, collection_name):
    conn = Connection(arangoURL=_arango_url, username=_arango_user, password=_arango_password)
    db = None
    if conn.hasDatabase(db_name):
        db = conn[db_name]
    else:
        db = conn.createDatabase(name=db_name)
    collection = None
    if db.hasCollection(collection_name):
        collection = db[collection_name]
    else:
        collection = db.createCollection(name=collection_name)
    return collection
