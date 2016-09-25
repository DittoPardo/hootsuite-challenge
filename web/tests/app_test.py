import pytest


@pytest.mark.options(debug=False)
def test_reddit_app(test_app):
    assert not test_app.debug, 'App is not in debug mode'
