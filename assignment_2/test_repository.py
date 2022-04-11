from pathlib import Path
import pytest
import tempfile

def _test_crud_url(db):
    db.put_url_and_user('key', 'http://example.com', 'user')
    assert db.has_url('key') is True
    assert db.get_url_and_user('key') == ('http://example.com', 'user')
    db.delete_url('key')
    assert db.get_url_and_user('key') is None
    assert db.has_url('key') is False

def _test_scan_keys(db):
    db.put_url_and_user('key_http_1', 'http://example.com', 'charlie')
    db.put_url_and_user('key_http_2', 'http://example.com', 'charlie')
    db.put_url_and_user('key_https_1', 'https://example.com', 'charlie')
    db.put_url_and_user('key_https_2', 'https://example.com', 'charlie')
    assert db.scan(lambda key, _: key.startswith('key_https')) == ['key_https_1', 'key_https_2']

def _test_scan_values(db):
    db.put_url_and_user('key1', 'http://example.com', 'alice')
    db.put_url_and_user('key2', 'http://example.com', 'alice')
    db.put_url_and_user('key3', 'http://example.com', 'alice')
    db.put_url_and_user('key4', 'http://example.com', 'bob')
    db.put_url_and_user('key5', 'http://example.com', 'bob')
    scan_result = db.scan(lambda _, value: value[1] == 'alice')
    assert len(scan_result) == 3
    assert 'key1' in scan_result
    assert 'key2' in scan_result
    assert 'key3' in scan_result

class TestRepositoryInMemory:
    @pytest.fixture
    def db(self):
        import repository_in_memory as db
        yield db

    def test_crud_url(self, db):
        _test_crud_url(db)

    def test_scan_keys(self, db):
        _test_scan_keys(db)

    def test_scan_values(self, db):
        _test_scan_values(db)

class TestRepositoryShelve:
    @pytest.fixture
    def db(self):
        import repository_shelve as db
        with tempfile.TemporaryDirectory() as directory:
            db.db_path = (Path(directory) / 'data').absolute()
            yield db
            db._close_db_if_open() # Write changes to disk before deleting temporary directory

    def test_crud_url(self, db):
        _test_crud_url(db)
    
    def test_scan_keys(self, db):
        _test_scan_keys(db)

    def test_scan_values(self, db):
        _test_scan_values(db)


