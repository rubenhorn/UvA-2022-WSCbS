from flask import Response
import json
import validators

mimetype = 'application/json'

def get_config(app, key, default=None):
    if key in app.config:
        return app.config[key]
    return default

def is_url_valid(url):
    return url is not None and validators.url(url)

def create_unique_url(user):
    # TODO implement
    raise NotImplementedError

def get_user(request, default=None):
    header_key = 'Authorization'
    user = request.headers.get(header_key)
    # TODO exctract user from JWT
    if user is None:
        user = default
    return user

def get_error_response(status_code, message):
    json_data = {'status': 'error', 'data': {'message': message}}
    return Response(json.dumps(json_data), status_code, mimetype=mimetype)

def get_data_response(status_code, data):
    json_data = {'status': 'success', 'data': data}
    return Response(json.dumps(json_data), status_code, mimetype=mimetype)

def url_from_request(request):
    try:
        return request.json['url']
    except Exception:
        return None
