import hashlib
import time
from flask import Response
import json
import uuid
import jwt
import validators

mimetype = 'application/json'
_jwt_secret = 'this_is_a_secret'
_app_secret = 'url-shortener-auth'

def get_config(app, key, default=None):
    if key in app.config:
        return app.config[key]
    return default

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
