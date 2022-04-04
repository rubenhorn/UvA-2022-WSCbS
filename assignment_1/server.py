from flask import Flask, request, Response
import json
import validators
import werkzeug.exceptions

app = Flask(__name__)

# ==================== UTILS ====================

mimetype = 'application/json'

def is_url_valid(url):
    return url is not None and validators.url(url)

def create_unique_url(user):
    # TODO implement
    raise NotImplementedError

def get_user(request):
    header_key = 'Authorization'
    user = request.headers.get(header_key)
    # TODO exctract user from JWT
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

# ==================== PARTIAL ROUTES ====================

def get_url(user, key):
    # TODO implement
    return get_error_response(404, 'Not found')

def update_url(user, key, new_url):
    if not is_url_valid(new_url):
        return get_error_response(400, 'Invalid URL')
    return get_error_response(404, 'Not found')

def delete_url(user, key):
    # TODO implement
    return get_error_response(404, 'Not found')

def get_keys(user):
    # TODO implement
    return get_data_response(200, { 'keys': [] })

def create_url(user, url):
    if not is_url_valid(url):
        return get_error_response(400, 'Invalid URL')
    # TODO implement
    return get_data_response(201, 'TODO')

# ==================== ROUTES ====================

@app.route('/<key>', methods=['GET', 'PUT', 'DELETE'])
def route_url(key):
    user = get_user(request)
    if user is None:
        res = get_error_response(401, 'Unauthorized')
    else:
        match request.method:
            case 'GET':
                res = get_url(user, key)
            case 'PUT':
                url = url_from_request(request)
                res = update_url(user, key, url)
            case 'DELETE':
                res = delete_url(user, key)
            case _:
                raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def route_keys():
    user = get_user(request)
    if user is None:
        res = get_error_response(401, 'Unauthorized')
    else:
        match request.method:
            case 'GET':
                res = get_keys(user)
            case 'POST':
                url = url_from_request(request)
                res = create_url(user, url)
            case 'DELETE':
                res = get_error_response(404, 'Nothing to delete')
            case _:
                raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res
