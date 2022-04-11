from flask import Flask, request
from flask_cors import CORS
from repository_policy import get_repository
import utils
import werkzeug.exceptions
import hashlib

app = Flask(__name__)
CORS(app)

# ==================== ROUTES ====================

@app.route('/users', methods=['POST'])
def route_users():
    credentials = utils.get_credentials_from_request(request)
    if credentials is None or utils.get_password_hash_from_db(credentials[0]) is not None:
        # todo: bad request (400)
        raise Exception
    utils.store_credentials_in_db(credentials)
    res = utils.get_data_response(200, None)
    return res


@app.route('/users/login', methods=['POST'])
def route_users():
    credentials = utils.get_credentials_from_request(request)
    try:
        hash_db = utils.get_password_hash_from_db(credentials[0])
        if hash_db != credentials[1]:
            raise Exception
    except:
        raise Exception # todo: return 403
    res = utils.get_data_response(200, {"bearer_token":utils.generate_token(credentials[0])})
    return res
