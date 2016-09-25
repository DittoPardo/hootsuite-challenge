import pytest

from reddit_web_app import create_app


@pytest.fixture
def test_app():
    app = create_app()

    return app
