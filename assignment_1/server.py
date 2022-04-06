from flask import Flask, request
from repository_policy import get_repository
import utils
import werkzeug.exceptions

app = Flask(__name__)

# ==================== PARTIAL ROUTES ====================

def get_url(key):
    if get_repository(app).has_url(key):
        url = get_repository(app).get_url_and_user(key)[0]
        return utils.get_redirect_response(url)
    return utils.get_error_response(404, 'Not found')

def update_url(user, key, new_url):
    if not utils.is_url_valid(new_url):
        return utils.get_error_response(400, 'Invalid URL')
    if get_repository(app).has_url(key):
        if get_repository(app).get_url_and_user(key)[1] != user:
            return utils.get_error_response(403, 'Forbidden')
        get_repository(app).put_url_and_user(key, new_url, user)
        return utils.get_data_response(200, None)
    return utils.get_error_response(404, 'Not found')

def delete_url(user, key):
    if get_repository(app).has_url(key):
        if get_repository(app).get_url_and_user(key)[1] != user:
            return utils.get_error_response(403, 'Forbidden')
        get_repository(app).delete_url(key)
        return utils.get_data_response(204, None)
    return utils.get_error_response(404, 'Not found')

def get_keys(user):
    keys = get_repository(app).scan(lambda _, value: value[1] == user)
    keys = [key[len(user) + 1:] for key in keys]
    return utils.get_data_response(200, { 'keys': keys })

def create_url(user, url):
    if not utils.is_url_valid(url):
        return utils.get_error_response(400, 'Invalid URL')
    key = utils.create_unique_id()
    get_repository(app).put_url_and_user(key, url, user)
    return utils.get_data_response(201, { 'id': key })

# ==================== ROUTES ====================

@app.route('/<key>', methods=['GET', 'PUT', 'DELETE'])
def route_url(key):
    user = utils.get_user(request, utils.get_config(app, 'DEFAULT_USER'))
    if request.method != 'GET' and user is None:
        res = utils.get_error_response(401, 'Unauthorized')
    else:
        match request.method:
            case 'GET':
                res = get_url(key)
            case 'PUT':
                url = utils.url_from_request(request)
                res = update_url(user, key, url)
            case 'DELETE':
                res = delete_url(user, key)
            case _:
                raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def route_keys():
    user = utils.get_user(request, utils.get_config(app, 'DEFAULT_USER'))
    if user is None:
        res = utils.get_error_response(401, 'Unauthorized')
    else:
        match request.method:
            case 'GET':
                res = get_keys(user)
            case 'POST':
                url = utils.url_from_request(request)
                res = create_url(user, url)
            case 'DELETE':
                res = utils.get_error_response(404, 'Nothing to delete')
            case _:
                raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res
