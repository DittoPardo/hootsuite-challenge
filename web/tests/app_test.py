import json
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


test_items_data = [
    (
        {'subreddit': 'python'},
        {'subreddit': 'python'}
    ),
    (
        {'subreddit': 'python', 'from': 1},
        {'subreddit': 'python',
         'created': {'$gte': 1},
        }
    ),
    (
        {'subreddit': 'python', 'to': 2},
        {'subreddit': 'python',
         'created': {'$lt': 2},
        }
    ),
    (
        {'subreddit': 'python', 'from': 1, 'to': 2},
        {'subreddit': 'python',
         'created': {'$gte': 1, '$lt': 2},
        }
    ),
    (
        {'subreddit': 'python', 'from': 1, 'to': 2, 'keyword': 'aa'},
        {'subreddit': 'python',
         'created': {'$gte': 1, '$lt': 2},
         '$text': {'$search': 'aa'},
        }
    ),
]


@pytest.mark.parametrize("get_params,expected_query", test_items_data)
def test_items(client, monkeypatch, mongo_mock, get_params, expected_query):
    mongo_mock.db.reddits.find.return_value = [
        {'id': 1},
        {'id': 2},
    ]
    monkeypatch.setattr('reddit_web_app.reddit_web_app.mongo', mongo_mock)
    resp = client.get(url_for('items', **get_params))
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    assert mongo_mock.db.reddits.find.called
    query, projection = mongo_mock.db.reddits.find.call_args[0]
    assert query == expected_query
    assert projection == {'_id': 0}

    # what's going on here? we don't even have content_encoding on this response.
    # flask/underling libs seem very un-python-3 here ...
    resp_json = json.loads(resp.data.decode('utf-8'))
    assert 'items' in resp_json
    items = resp_json['items']
    assert len(items) == 2
    item1 = items[0]
    assert 'id' in item1
    assert item1['id'] == 1
