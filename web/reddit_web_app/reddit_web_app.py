import os

from flask import Flask, request, url_for
from redis import Redis

debug = bool(os.environ.get('HSC_DEBUG', False))

redis = Redis(host='redis', port=6379)


def create_app(config_filename=None):
    app = Flask(__name__)

    return app


app = create_app()


@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen {} times'.format(int(redis.get('hits')))


@app.route('/items')
def items():
    return 'items'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug)
