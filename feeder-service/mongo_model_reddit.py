import pymongo
from settings import (
    MONGO_HOST,
)


class MongoReddit(object):
    def __init__(self):
        self.mongo_client = pymongo.MongoClient(host=MONGO_HOST)
        self.db = self.mongo_client.hsc
        self.reddit_collection = self.db.reddits
        self._setup_indexes()

    def _setup_indexes(self, background=False):
        # TODO It's weird to set this up every time... but for starters...
        # set to separate indexes. These should be intersectable
        self.reddit_collection.create_index(
            [("subreddit", pymongo.ASCENDING)],
            background=background
        )
        self.reddit_collection.create_index(
            [("created", pymongo.DESCENDING)],
            background=background,
        )
        # not much sense in ascending here... use hashed?
        # TODO don't know whether this is unique across reddit. Use compound(subreddit, id) instead?
        # TODO Use this on _id instead of ObjectId?
        self.reddit_collection.create_index(
            [("id", pymongo.ASCENDING)],
            background=background,
            unique=True,
        )
        # we shall do text search by these fields
        self.reddit_collection.create_index(
            [("title", pymongo.TEXT), ("text", pymongo.TEXT)],
            background=background,
        )
        # a good sharding key would probably be {subreddit: 1, _id: -1}
        # Ideally we would compound sharding key with a hashed index but that is not supported as of mongo 3.2
        # Let's just consider this premature optimization though - One can lose quite some time investigating sharding

    def close(self):
        self.mongo_client.close()

    def update_or_insert(self, doc):
        # TODO handle non-optimistic paths here
        result = self.reddit_collection.replace_one(
            {'id': doc['id']},
            doc,
            upsert=True,
        )
        # TODO This will create a brand new object with a new _id even on 'update' case... Result doesn't know that _id
        return result.modified_count, result.upserted_id

    def fetch(self, query, projection=None, limit=0):
        return self.reddit_collection.find(query, projection, limit=limit)

