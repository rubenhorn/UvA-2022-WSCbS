import pytest
import utils

class TestBase:
    @pytest.fixture
    def client(self):
        from auth_server import app
        app.config['EPHEMERAL'] = True # Do not use persistent storage for testing
        client = app.test_client()
        yield client

class TestInterface(TestBase):
    def test_registration_without_credentials_should_fail(self, client):
        response = client.post('/users')
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Invalid request body' }

    def test_registering_existing_username_should_fail(self, client):
        response = client.post('/users', json={ 'username': 'alice', 'password': 'test' })
        assert response.status_code == 200
        response = client.post('/users', json={ 'username': 'alice', 'password': 'test' })
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'User already exists' }

    def test_registering_new_user_should_succeed(self, client):
        response = client.post('/users', json={ 'username': 'bob', 'password': 'test' })
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data'] == None

    def test_login_with_invalid_credentials_should_fail(self, client):
        response = client.post('/users/login', json={ 'username': 'bob', 'password': 'wrong' })
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['data'] == { 'message': 'Invalid credentials' }

    def test_login_with_valid_credentials_should_succeed(self, client):
        response = client.post('/users', json={ 'username': 'charlie', 'password': 'test' })
        assert response.status_code == 200
        response = client.post('/users/login', json={ 'username': 'charlie', 'password': 'test' })
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert utils.user_from_token(response.json['data']['bearer_token']) == 'charlie'
