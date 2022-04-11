from flask import Flask, Request
import json
import utils

class TestUtils:
    def test_get_config_should_return_value_from_config(self):
        app = Flask('test')
        app.config['FOO'] = 'bar'
        assert utils.get_config(app, 'FOO') == 'bar'

    def test_get_config_should_return_default_value_if_key_not_in_config(self):
        app = Flask('test')
        assert utils.get_config(app, 'FOO', 'bar') == 'bar'

    def test_validating_valid_url_should_return_true(self):
        assert utils.is_url_valid('http://example.com') is True

    def test_validating_invalid_url_should_return_false(self):
        assert utils.is_url_valid('example.com') is False

    def test_id_should_be_8_characters_long(self):
        assert len(utils.create_unique_id()) == 8

    # Flaky (collisions are possible)
    def test_id_should_be_unique(self):
        ids = set()
        for _ in range(10000):
            id = utils.create_unique_id()
            assert id not in ids
            ids.add(id)

    def test_error_response_follows_jsend_format(self):
        response = utils.get_error_response(400, 'Bad Request')
        assert response.status_code == 400
        assert response.mimetype == 'application/json'
        assert response.data == b'{"status": "error", "data": {"message": "Bad Request"}}'

    def test_data_response_follows_jsend_format(self):
        response = utils.get_data_response(200, {'foo': 'bar'})
        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        assert response.data == b'{"status": "success", "data": {"foo": "bar"}}'

    def test_redirect_response_follows_jsend_format(self):
        response = utils.get_redirect_response('http://example.com')
        assert response.status_code == 301
        assert response.mimetype == 'application/json'
        assert response.headers['Location'] == 'http://example.com'
        assert response.data == b'{"status": "success", "data": {"url": "http://example.com"}}'

    def test_extract_url_from_request_body_containing_url(self):
        json_body = {'url': 'http://example.com'}
        request = Request.from_values(method='POST', json=json_body)
        assert utils.url_from_request(request) == 'http://example.com'

    def test_extract_none_from_request_body_containing_no_url(self):
        request = Request.from_values(method='POST')
        assert utils.url_from_request(request) is None
