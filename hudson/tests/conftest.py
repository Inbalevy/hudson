import pytest
from hudson.app import create_app

@pytest.fixture(scope='session', autouse=True)
def app():
    app = create_app()
    app.config["TESTING"] = True
    yield app