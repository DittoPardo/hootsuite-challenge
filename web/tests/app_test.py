from flask import url_for, request
import pytest
from unittest.mock import Mock


@pytest.mark.options(debug=False)
def test_app_debug_off(app):
    assert not app.debug, 'App is in debug mode'


@pytest.mark.options(debug=True)
def test_app_debug_on(app):
    assert app.debug, 'App is not in debug mode'


def test_hello(client, monkeypatch, redis_mock):
    redis_mock.get.return_value = 1
    monkeypatch.setattr('reddit_web_app.reddit_web_app.redis', redis_mock)
    resp = client.get(url_for('hello'))
    assert b'I have been seen 1 times' in resp.data


def test_items(client):
    resp = client.get(url_for('items'))
    assert b'items' in resp.data
