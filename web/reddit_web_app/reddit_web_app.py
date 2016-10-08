import os

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
    url_for,
)
from flask_pymongo import PyMongo
from redis import Redis

debug = bool(os.environ.get('HSC_DEBUG', False))

redis = Redis(host='redis', port=6379)


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    return app


app = create_app()
mongo = PyMongo(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen {} times'.format(int(redis.get('hits')))


@app.route('/items', methods=['GET'])
def items():
    subreddit = request.args['subreddit']
    from_ts = int(request.args['from'])
    to_ts = int(request.args['to'])
    keyword = request.args.get('keyword', None)
    query = {
        'subreddit': subreddit,
        'created': {'$gte': from_ts, '$lt': to_ts},
    }
    if keyword:
        query['$text'] = {"$search": keyword}
    reddit_items = mongo.db.reddits.find(query, {
        '_id': 0,
    })
    return jsonify({'items': list(reddit_items)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug)
