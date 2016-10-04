import json

import praw
from pymongo import MongoClient

from settings import (
    MONGO_HOST,
    REDDIT_UA,
)


class RedditReader(object):
    def __init__(self, mongo_host=MONGO_HOST):
        self.reddit_ua = REDDIT_UA
        self.mongo_host = mongo_host
        # TODO this should not be here... turn mongo_client into our own class with these responsabilities
        self.mongo_db = 'hsc'
        self.mongo_collection = 'reddits'

    def __enter__(self):
        # TODO We need to setup indexes on mongo collection in order to insert or update
        self.mongo_client = MongoClient(host=self.mongo_host)
        self.reddit_client = praw.Reddit(user_agent=self.reddit_ua)
        return self

    def __exit__(self):
        self.mongo_client.close()

    # read from reddit, process data, store in mongo
    def consume_subreddit(self, subreddit):
        subr = self.reddit_client.get_subreddit(subreddit).get_top(limit=10)
        for submission in subr:
            mongo_obj_submission = RedditSubmission(submission)
            #add or replace submission to mongo
            for comment in submission.comments:
                # TODO replies to comments are nested even farther down ?
                mongo_obj_comment = RedditComment(comment)
                #add or replace comment to mongo


class RedditObject(object):
    def __init__(self, r_object):
        self.mobj_id = r_object.id
        self.mobj_author = {
            'id': r_object.author.id,
            'name': r_object.author.name,
        }

    def to_mongo_obj(self):
        # This goes only one level depth. Make sure that nested objects are jsonable
        jsonable = {}
        for key in (mobj_key for mobj_key in self.__dict__ if mobj_key.startswith('mobj_')):
            mongo_key = key[len('mobj_'):]
            jsonable[mongo_key] = getattr(self, key)
        return jsonable


class RedditSubmission(RedditObject):
    def __init__(self, r_submission):
        super().__init__(r_submission)
        self.mobj_type = 'submission'
        self.mobj_parent_id = r_submission.subreddit_id
        # link high up
        self.mobj_subreddit_id = r_submission.subreddit_id
        self.mobj_comments_ids = [c.id for c in r_submission.comments]
        self.mobj_title = r_submission.title
        # there's also selftext on sumissions


class RedditComment(RedditObject):
    def __init__(self, r_comment):
        super().__init__(r_comment)
        self.mobj_type = 'comment'
        # TODO can the parent be another comment, apparently there is a parent_id on comment of form xx_<submission_id>
        self.mobj_parent_id = r_comment.submission.id
        # link high up
        self.mobj_subreddit_id = r_comment.subreddit_id
        self.mobj_text = r_comment.body
