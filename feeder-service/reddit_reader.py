import json

import praw
import sys

from mongo_model_reddit import MongoReddit
from settings import (
    REDDIT_UA,
)


class RedditReader(object):
    def __init__(self):
        self.reddit_ua = REDDIT_UA

    def __enter__(self):
        self.mongo_client = MongoReddit()
        self.reddit_client = praw.Reddit(user_agent=self.reddit_ua)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reddit_client.clear_authentication()
        self.mongo_client.close()
        if exc_type:
            print(exc_type, exc_value, file=sys.stderr)
        return True

    # read from reddit, process data, store in mongo
    def consume_subreddit(self, subreddit):
        subr = self.reddit_client.get_subreddit(subreddit)
        submissions = subr.get_new(limit=25)
        for submission in submissions:
            mongo_obj_submission = RedditSubmission(submission)
            self.mongo_client.update_or_insert(mongo_obj_submission.to_mongo_obj())
            # TODO We should use subreddit.get_comments() to get recent comments from everywhere...
            for comment in praw.helpers.flatten_tree(submission.comments):
                mongo_obj_comment = RedditComment(comment)
                self.mongo_client.update_or_insert(mongo_obj_comment.to_mongo_obj())


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
        # limit this to 10, it a tree of comments and some objects are MoreComment, so this needs change anyway
        #self.mobj_comments_ids = [c.id for c in r_submission.comments[:10]]
        self.mobj_title = r_submission.title
        # there's also selftext on sumissions


class RedditComment(RedditObject):
    def __init__(self, r_comment):
        super().__init__(r_comment)
        self.mobj_type = 'comment'
        # TODO this is wrong, the parent can be another comment,
        # however there is a parent_id on comment of form xx_<submission_id>, so not quite the id we are looking for
        self.mobj_parent_id = r_comment.submission.id
        # link high up
        self.mobj_subreddit_id = r_comment.subreddit_id
        self.mobj_text = r_comment.body
