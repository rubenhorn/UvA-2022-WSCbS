from http.client import BAD_REQUEST, CREATED, FORBIDDEN, NO_CONTENT, NOT_FOUND, OK, UNAUTHORIZED
from flask import Flask, request
from flask_cors import CORS
from repository_policy import get_repository
import utils
import werkzeug.exceptions

app = Flask(__name__)
CORS(app)

# ==================== PARTIAL ROUTES ====================

def get_url(key):
    if get_repository(app).has_url(key):
        url = get_repository(app).get_url_and_user(key)[0]
        return utils.get_redirect_response(url)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def update_url(user, key, new_url):
    if not utils.is_url_valid(new_url):
        return utils.get_error_response(BAD_REQUEST, 'Invalid URL')
    if get_repository(app).has_url(key):
        if get_repository(app).get_url_and_user(key)[1] != user:
            return utils.get_error_response(FORBIDDEN, 'Forbidden')
        get_repository(app).put_url_and_user(key, new_url, user)
        return utils.get_data_response(OK, None)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def delete_url(user, key):
    if get_repository(app).has_url(key):
        if get_repository(app).get_url_and_user(key)[1] != user:
            return utils.get_error_response(FORBIDDEN, 'Forbidden')
        get_repository(app).delete_url(key)
        return utils.get_data_response(NO_CONTENT, None)
    return utils.get_error_response(NOT_FOUND, 'Not found')

def get_keys(user):
    keys = get_repository(app).scan(lambda _, value: value[1] == user)
    keys_and_urls = [{ 'key': key, 'url': str(get_repository(app).get_url_and_user(key)[0]) } for key in keys]
    return utils.get_data_response(OK, { 'shortened_urls': keys_and_urls })

def create_url(user, url):
    if not utils.is_url_valid(url):
        return utils.get_error_response(BAD_REQUEST, 'Invalid URL')
    key = utils.create_unique_id()
    get_repository(app).put_url_and_user(key, url, user)
    return utils.get_data_response(CREATED, { 'id': key })

# ==================== ROUTES ====================

@app.route('/<key>', methods=['GET', 'PUT', 'DELETE'])
def route_url(key):
    user = utils.get_user(request, utils.get_config(app, 'DEFAULT_USER'))
    if request.method != 'GET' and user is None:
        res = utils.get_error_response(FORBIDDEN, 'Forbidden')
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
        res = utils.get_error_response(FORBIDDEN, 'Forbidden')
    else:
        match request.method:
            case 'GET':
                res = get_keys(user)
            case 'POST':
                url = utils.url_from_request(request)
                res = create_url(user, url)
            case 'DELETE':
                res = utils.get_error_response(NOT_FOUND, 'Nothing to delete')
            case _:
                raise werkzeug.exceptions.InternalServerError('Unhandled case')
    return res
