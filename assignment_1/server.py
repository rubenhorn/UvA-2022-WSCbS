from flask import Flask, request
import werkzeug.exceptions
import utils

app = Flask(__name__)

# ==================== PARTIAL ROUTES ====================

def get_url(user, key):
    # TODO implement
    return utils.get_error_response(404, 'Not found')

def update_url(user, key, new_url):
    if not utils.is_url_valid(new_url):
        return utils.get_error_response(400, 'Invalid URL')
    return utils.get_error_response(404, 'Not found')

def delete_url(user, key):
    # TODO implement
    return utils.get_error_response(404, 'Not found')

def get_keys(user):
    # TODO implement
    return utils.get_data_response(200, { 'keys': [] })

def create_url(user, url):
    if not utils.is_url_valid(url):
        return utils.get_error_response(400, 'Invalid URL')
    # TODO implement
    return utils.get_data_response(201, 'TODO')

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
