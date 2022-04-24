import pytest
import utils

test_url = 'https://www.example.org'
test_auth_header_a = 'Bearer ' + utils.generate_token('alice')
test_auth_header_b = 'Bearer ' + utils.generate_token('bob')
test_key_exists = None
test_key_not_exists = 'foo'

class TestBase:
    @pytest.fixture
    def client(self):
        global test_key_exists
        from app_server import app
        app.config['DEFAULT_USER'] = None
        app.config['EPHEMERAL'] = True # Do not use persistent storage for testing
        client = app.test_client()
        response = client.post('/', json={'url': test_url}, headers={'Authorization': test_auth_header_a})
        test_key_exists = response.json['data']['id']
        yield client

class TestInterface(TestBase):
    def test_unauthorized_request_should_fail(self, client):
        response = client.get('/')
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Forbidden' }

    def test_get_non_existing_key_should_fail(self, client):
        response = client.get(f'/{test_key_not_exists}')
        assert response.status_code == 404

    def test_get_existing_key_should_succeed(self, client):
        response = client.get(f'/{test_key_exists}')
        print(test_key_exists)
        assert response.status_code == 301
        assert response.headers['Location'] == test_url

    def test_update_non_existing_key_should_fail(self, client):
        response = client.put(f'/{test_key_not_exists}', json={'url': test_url}, headers={'Authorization': test_auth_header_a})
        assert response.status_code == 404

    def test_update_existing_key_invalid_url_should_fail(self, client):
        response = client.put(f'/{test_key_exists}', json={'url': 'foo'}, headers={'Authorization': test_auth_header_a})
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Invalid URL' }

    def test_update_existing_key_valid_url_should_succeed(self, client):
        new_url = 'https://www.google.com'
        response = client.put(f'/{test_key_exists}', json={'url': new_url}, headers={'Authorization': test_auth_header_a})
        assert response.status_code == 200
        response = client.get(f'/{test_key_exists}')
        assert response.status_code == 301
        assert response.headers['Location'] == new_url

    def test_delete_non_existing_key_should_fail(self, client):
        response = client.delete(f'/{test_key_not_exists}', headers={'Authorization': test_auth_header_a})
        assert response.status_code == 404

    def test_delete_existing_key_should_succeed(self, client):
        global test_key_exists
        response = client.delete(f'/{test_key_exists}', headers={'Authorization': test_auth_header_a})
        assert response.status_code == 204
        response = client.post('/', json={'url': test_url}, headers={'Authorization': test_auth_header_a})
        test_key_exists = response.json['data']['id']

    def test_modify_other_user_should_fail(self, client):
        response = client.put(f'/{test_key_exists}', json={'url': test_url}, headers={'Authorization': test_auth_header_b})
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Forbidden' }
        response = client.delete(f'/{test_key_exists}', headers={'Authorization': test_auth_header_b})
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Forbidden' }

    def test_get_keys_from_root_should_succeed(self, client):
        response = client.get('/', headers={'Authorization': test_auth_header_a})
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert type(response.json['data']['shortened_urls']) == list
        list_item = response.json['data']['shortened_urls'][0]
        assert type(list_item['key']) == str
        assert type(list_item['url']) == str

    def test_create_key_should_succeed(self, client):
        response = client.post('/', json={'url': test_url}, headers={'Authorization': test_auth_header_a})
        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert type(response.json['data']['id']) == str

    def test_create_key_with_invalid_url_should_fail(self, client):
        response = client.post('/', json={'url': 'foo'}, headers={'Authorization': test_auth_header_a})
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Invalid URL' }

    def test_delete_root_should_fail(self, client):
        response = client.delete('/', headers={'Authorization': test_auth_header_a})
        assert response.status_code == 404
