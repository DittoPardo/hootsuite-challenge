import os

from flask import (
    Flask,
    jsonify,
    make_response,
    render_template,
    request,
    url_for,
)
from flask_pymongo import PyMongo
from flask_webpack import Webpack
from redis import Redis

g_debug = bool(os.environ.get('HSC_DEBUG', False))
g_testing = bool(os.environ.get('HSC_TEST', False))
webpack = Webpack()

redis = Redis(host='redis', port=6379)


def create_app():
    app = Flask('reddit_web_app', template_folder='templates')
    app.config.from_envvar('FLASK_REDDIT_SETTINGS')
    app.config['DEBUG'] = g_debug
    webpack.init_app(app)

    return app


app = create_app()
mongo = PyMongo(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello():
    redis.incr('hits')
    times = int(redis.get('hits'))
    return render_template('index.html', times=times)


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
    app.run(host='0.0.0.0', debug=g_debug, use_reloader=g_debug, use_debugger=g_debug)
