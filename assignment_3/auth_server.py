from http.client import BAD_REQUEST, FORBIDDEN, OK
from flask import Flask, request
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)

DB_NAME = 'auth_service'
COLLECTION_NAME = 'credentials'

def store_credentials_in_db(user_credentials):
    credentials = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    doc = None
    try:
        doc = credentials[user_credentials[0]]
    except:
        pass
    if doc is None:
        doc = credentials.createDocument()
    doc._key = user_credentials[0]
    doc['hash'] = user_credentials[1]
    doc.save()

def get_password_hash_from_db(username):
    credentials = utils.get_database_collection(DB_NAME, COLLECTION_NAME)
    try:
        return credentials[username]['hash']
    except:
        return None

# ==================== ROUTES ====================

@app.route('/users', methods=['POST'])
def register():
    credentials = utils.get_credentials_from_request(request)
    if credentials is None:
        return utils.get_error_response(BAD_REQUEST, 'Invalid request body')
    if get_password_hash_from_db(credentials[0]) is not None:
        return utils.get_error_response(BAD_REQUEST, 'User already exists')
    store_credentials_in_db(credentials)
    return utils.get_data_response(OK, None)


@app.route('/users/login', methods=['POST'])
def login():
    credentials = utils.get_credentials_from_request(request)
    try:
        hash_db = get_password_hash_from_db(credentials[0])
        if hash_db != credentials[1]:
            raise Exception
    except:
        return utils.get_error_response(FORBIDDEN, 'Invalid credentials')
    return utils.get_data_response(OK, { 'bearer_token': utils.generate_token(credentials[0])})
