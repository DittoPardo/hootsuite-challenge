import pytest
from redis import Redis
from unittest.mock import Mock

from reddit_web_app import reddit_web_app


@pytest.fixture
def app():
    app = reddit_web_app.create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'

    return app


@pytest.fixture
def client(request):
    print(" +++++++++ init client fixture")
    reddit_web_app.app.config['TESTING'] = True
    reddit_web_app.app.config['SERVER_NAME'] = 'localhost:5000'
    client = reddit_web_app.app.test_client()

    def teardown():
        print(" ------- Tearing down")

    request.addfinalizer(teardown)
    with reddit_web_app.app.app_context():
        yield client


@pytest.fixture
def redis_mock():
    return Mock(spec=Redis)

