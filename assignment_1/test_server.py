import pytest

@pytest.fixture
def client():
    from server import app
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_get_non_existing_key_should_fail(client):
    response = client.get('/foo')
    assert response.status_code == 404

def test_get_existing_key_should_succeed(client):
    response = client.get('/foo')
    assert response.status_code == 301
    assert response.headers['Location'] == 'https://www.google.com'

def test_update_non_existing_key_should_fail(client):
    response = client.put('/foo')
    assert response.status_code == 404

def test_update_existing_key_invalid_url_should_fail(client):
    response = client.put('/foo', data={'url': 'foo'})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['data'] == { 'message': 'Invalid URL' }

def test_update_existing_key_valid_url_should_succeed(client):
    new_url = 'https://www.google.com'
    response = client.put('/foo', data={'url': new_url})
    assert response.status_code == 200
    response = client.get('/foo')
    assert response.status_code == 301
    assert response.headers['Location'] == new_url

def test_delete_non_existing_key_should_fail(client):
    response = client.delete('/foo')
    assert response.status_code == 404

def test_delete_existing_key_should_succeed(client):
    response = client.delete('/foo')
    assert response.status_code == 204

def test_get_keys_from_root_should_succeed(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data'] == ['Foo']

def test_create_key_should_succeed(client):
    response = client.post('/', data={'url': 'https://www.google.com'})
    assert response.status_code == 201
    assert response.json['status'] == 'success'
    assert response.json['data'] == { 'id': 'foo' }

def test_create_key_with_invalid_url_should_fail(client):
    response = client.post('/', data={'url': 'foo'})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['data'] == { 'message': 'Invalid URL' }

def test_delete_root_should_fail(client):
    response = client.delete('/')
    assert response.status_code == 404

