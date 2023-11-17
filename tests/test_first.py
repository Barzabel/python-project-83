import pytest
from page_analyzer.app import app as application

@pytest.fixture()
def flask_app():
    app = application
    yield app

@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def runner(flask_app):
    return flask_app.test_cli_runner()


def test_request_example(client):
    response = client.get("/")
    assert b"Анализатор страниц" in response.data
