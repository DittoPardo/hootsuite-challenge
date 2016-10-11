import json
from unittest.mock import Mock

from praw.objects import Comment, Submission
import pytest

from reddit_reader import RedditSubmission, RedditComment


class TestRedditObject(object):
    @pytest.fixture
    def comment(self):
        com = Mock(spec=Comment)
        com.id = 'comment_id_1'
        com.created = 22
        com.author = Mock(id='author_id_2')
        com.author.name = 'author_2'
        com.subreddit_id = 'subreddit_id_1'
        com.submission = Mock(id='submission_id_1')  # linked with the submission below
        com.body = 'comment body 1'
        return com

    @pytest.fixture
    def submission(self, comment):
        sub = Mock(spec=Submission)
        sub.id = 'submission_id_1'
        sub.created = 11
        sub.author = Mock(id='author_id_1')
        sub.author.name = 'author_1'
        sub.subreddit_id = 'subreddit_id_1'
        sub.title = 'title 1'
        sub.comments = [comment]
        return sub

    def test_subbmission(self, submission):
        rs = RedditSubmission(submission, subreddit='python')
        mongo_object = rs.to_mongo_obj()
        # make sure this is a jsonable dict
        json.dumps(mongo_object)
        expected_obj = {
            'author': {
                'id': 'author_id_1',
                'name': 'author_1'
            },
            #'comments_ids': ['comment_id_1'],
            'id': 'submission_id_1',
            'subreddit': 'python',
            'created': 11,
            'parent_id': 'subreddit_id_1',
            'subreddit_id': 'subreddit_id_1',
            'title': 'title 1',
            'type': 'submission'
        }
        assert mongo_object == expected_obj

    def test_comment(self, comment):
        rc = RedditComment(comment, subreddit='python')
        mongo_object = rc.to_mongo_obj()
        # make sure this is a jsonable dict
        json.dumps(mongo_object)
        expected_obj = {
            'author': {
                'id': 'author_id_2',
                'name': 'author_2'
            },
            'id': 'comment_id_1',
            'subreddit': 'python',
            'created': 22,
            'parent_id': 'submission_id_1',
            'subreddit_id': 'subreddit_id_1',
            'text': 'comment body 1',
            'type': 'comment'
        }
        assert mongo_object == expected_obj

