import os
from reddit_automation_suite.reddit_utils import (
    get_permalink,
    get_user_as_string,
    has_stickied_comment,
    PluginBase,
)
from .mocks.reddit_objects import Redditor, Submission, Comment


def test_get_permalink():
    submission_id = "1a2b3cd"
    assert get_permalink(submission_id) == "https://redd.it/1a2b3cd"

    submission_id = None
    assert get_permalink(submission_id) == None

    submission_id = "/r/MySubreddit/comments/1a2b3cd/My_Post_title/"
    assert get_permalink(submission_id) == "https://redd.it/1a2b3cd"


def test_get_user_as_string():
    redditor = Redditor(name="Frank123")
    submission = Submission(author=redditor, permalink=None, id=None, comments=None)
    assert get_user_as_string(submission) == "Frank123"

    submission = Submission(author=None, permalink=None, id=None, comments=None)

    assert get_user_as_string(submission) == "[Unable to find user]"


def test_has_stickied_comment():
    submission = Submission(author=None, permalink=None, id=None, comments=[])

    assert has_stickied_comment(submission) == False

    redditor = Redditor(name="Frank123")
    comment_a = Comment(body=None, stickied=True, distinguished=True, author=redditor)
    comment_b = Comment(body=None, stickied=True, distinguished=False, author=None)
    submission = Submission(
        author=None, permalink=None, id=None, comments=[comment_a, comment_b]
    )
    assert has_stickied_comment(submission) == True

    submission = Submission(author=None, permalink=None, id=None, comments=[comment_b])

    assert has_stickied_comment(submission) == False

    submission = Submission(author=None, permalink=None, id=None, comments=[comment_a])
    assert has_stickied_comment(submission, moderator_name="Frank123") == True
    assert has_stickied_comment(submission, moderator_name="Bob321") == False


def test_load_config():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    assert plugin.config.get("test")


def test_config():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    assert plugin.config == plugin.load_config()


def test_consume_comment():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    plugin.consume_comment(None)


def test_consume_submission():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    plugin.consume_submission(None)


def test_consume_mod_log():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    plugin.consume_mod_log(None)


def test_consume_modmail():
    config_path = os.path.join(os.path.dirname(__file__), "./mocks/config.yaml")
    plugin = PluginBase(config_path=config_path)
    plugin.consume_modmail(None)
