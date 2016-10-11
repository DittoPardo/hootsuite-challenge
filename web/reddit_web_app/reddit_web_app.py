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

g_debug = bool(os.environ.get('HSC_DEBUG', False))
g_testing = bool(os.environ.get('HSC_TEST', False))

redis = Redis(host='redis', port=6379)


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('FLASK_REDDIT_SETTINGS')

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
    # TODO make this part of the rest path
    subreddit = request.args['subreddit']
    from_ts = int(request.args.get('from', 0))
    to_ts = int(request.args.get('to', 0))
    keyword = request.args.get('keyword', None)

    created_q = {}
    if from_ts:
        created_q['$gte'] = from_ts
    if to_ts:
        created_q['$lt'] = to_ts

    query = {
        'subreddit': subreddit,
    }
    if created_q:
        query['created'] = created_q
    if keyword:
        query['$text'] = {"$search": keyword}
    reddit_items = mongo.db.reddits.find(query, {
        '_id': 0,
    })
    return jsonify({'items': list(reddit_items)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=g_debug)
