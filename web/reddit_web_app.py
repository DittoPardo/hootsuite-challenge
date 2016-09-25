import os

from flask import Flask
from redis import Redis

debug = bool(os.environ.get('HSC_DEBUG', False))

redis = Redis(host='redis', port=6379)


def create_app(config_filename=None):
    app = Flask(__name__)

    return app


web_app = create_app()


@web_app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen {} times'.format(int(redis.get('hits')))

if __name__ == '__main__':
    web_app.run(host='0.0.0.0', debug=debug)
