import pytest


@pytest.fixture(scope='function', autouse=True)
def set_testing(monkeypatch):
    """Sets the TESTING environment variable."""
    monkeypatch.setenv('TESTING', '')
