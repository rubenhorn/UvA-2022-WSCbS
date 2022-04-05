from flask import Flask, request
from repository_policy import get_repository
import utils
import werkzeug.exceptions

app = Flask(__name__)

# ==================== PARTIAL ROUTES ====================

def get_url(user, key):
    if get_repository(app).has_url(f'{user}/{key}'):
        url = get_repository(app).get_url(f'{user}/{key}')
        return utils.get_redirect_response(url)
    return utils.get_error_response(404, 'Not found')

def update_url(user, key, new_url):
    if not utils.is_url_valid(new_url):
        return utils.get_error_response(400, 'Invalid URL')
    if get_repository(app).has_url(f'{user}/{key}'):
        get_repository(app).put_url(f'{user}/{key}', new_url)
        return utils.get_data_response(200, None)
    return utils.get_error_response(404, 'Not found')

def delete_url(user, key):
    if get_repository(app).has_url(f'{user}/{key}'):
        get_repository(app).delete_url(f'{user}/{key}')
        return utils.get_data_response(204, None)
    return utils.get_error_response(404, 'Not found')

def get_keys(user):
    keys = get_repository(app).scan_keys(lambda key: key.startswith(user))
    keys = [key[len(user) + 1:] for key in keys]
    return utils.get_data_response(200, { 'keys': keys })

def create_url(user, url):
    if not utils.is_url_valid(url):
        return utils.get_error_response(400, 'Invalid URL')
    shortened_url = f'/{utils.create_unique_id()}'
    key = f'{user}{shortened_url}'
    get_repository(app).put_url(key, url)
    return utils.get_data_response(201, { 'id': shortened_url[1:] })

# ==================== ROUTES ====================

@app.route('/<key>', methods=['GET', 'PUT', 'DELETE'])
def route_url(key):
    user = utils.get_user(request, utils.get_config(app, 'DEFAULT_USER'))
    if user is None:
        res = utils.get_error_response(401, 'Unauthorized')
    else:
        match request.method:
            case 'GET':
                res = get_url(user, key)
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
