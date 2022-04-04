from flask import Flask, request, Response
from markupsafe import escape
import validators
import werkzeug.exceptions

app = Flask(__name__)

def is_url_valid(url):
    return validators.url(url)

def get_user(request):
    header_key = 'Authorization'
    user = request.headers.get(header_key)
    # TODO exctract user from JWT
    return user

mimetype = 'application/json'

def get_key(user, id):
    pass

def update_key(user, id, new_url):
    pass

def delete_key(user, id):
    pass

def get_keys(user):
    print(f'getting keys for user {user}')
    return 'Foo'

def create_key(user, url):
    pass

# ================== ROUTES ====================

@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def key(id):
    user = get_user(request)
    status = 200
    if(not is_url_valid(id)):
        data = {'error': 'Invalid URL'}
        status = 400
    else:
        match request.method:
            case 'GET':
                data, status = get_key(user, id)
            case 'PUT':
                data, status = update_key(user, id)
            case 'DELETE':
                data, status = delete_key(user, id)
    return Response(data, mimetype = mimetype, status=status)

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def keys():
    user = get_user(request)
    status = 200
    match request.method:
        case 'GET':
            data, status = get_keys(user)
        case 'PUT':
            data, status = create_key(user)
        case 'DELETE':
            raise werkzeug.exceptions.NotFound()
    return Response(data, mimetype = mimetype, status=status)
