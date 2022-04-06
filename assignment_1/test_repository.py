from pathlib import Path
import pytest
import tempfile

def _test_crud_url(db):
    db.put_url('user/key', 'http://example.com')
    assert db.has_url('user/key') is True
    assert db.get_url('user/key') == 'http://example.com'
    db.delete_url('user/key')
    assert db.get_url('user/key') is None
    assert db.has_url('user/key') is False

def _test_scan_keys(db):
    db.put_url('alice/key1', 'http://example.com')
    db.put_url('alice/key2', 'http://example.com')
    db.put_url('alice/key3', 'http://example.com')
    db.put_url('bob/key1', 'http://example.com')
    db.put_url('bob/key2', 'http://example.com')
    assert db.scan_keys(lambda key: key.startswith('alice')) == ['alice/key1', 'alice/key2', 'alice/key3']

class TestRepositoryInMemory:
    @pytest.fixture
    def db(self):
        import repository_in_memory as db
        yield db

    def test_crud_url(self, db):
        _test_crud_url(db)

    def test_scan_keys(self, db):
        _test_scan_keys(db)

class TestRepositoryShelve:
    @pytest.fixture
    def db(self):
        import repository_shelve as db
        with tempfile.TemporaryDirectory() as directory:
            db.db_path = (Path(directory) / 'data').absolute()
            yield db

    def test_crud_url(self, db):
        _test_crud_url(db)

    def test_scan_keys(self, db):
        _test_scan_keys(db)


