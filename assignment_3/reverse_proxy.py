# (!) This is just a naive proof of concept. PLEASE use nginx or similar in production.

from flask import Flask, request, Response
import requests

prefix_mapping = {
    'users': 'http://localhost:5001', # Auth
    '': 'http://localhost:5002', # URL shortener
    'gui': 'http://localhost:5003', # Frontend
}

def map_prefix_to_target(request_path):
    longest_prefix = ''
    for prefix in prefix_mapping:
        if request_path.startswith(prefix) and len(prefix) > len(longest_prefix):
            longest_prefix = prefix
    return prefix_mapping[longest_prefix] + '/'

app = Flask(__name__)

methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    
@app.route('/', defaults={'req_path': ''},  methods=methods)
@app.route('/<path:req_path>',  methods=methods)
def proxy(req_path):
    response = requests.request(
        request.method,
        map_prefix_to_target(req_path) + req_path,
        headers=request.headers,
        data=request.data,
        params=request.args,
        cookies=request.cookies,
        allow_redirects=False
    )
    return Response(response.content, response.status_code, response.headers.items())
