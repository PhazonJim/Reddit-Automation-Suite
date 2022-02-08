import os
import logging
from ...reddit_utils import PluginBase


class Foo(PluginBase):
    def __init__(self, reddit, subreddit):
        PluginBase.__init__(
            self,
            name="Example",
            reddit=reddit,
            subreddit=subreddit,
            config_path=os.path.join(os.path.dirname(__file__), "config.yaml"),
        )

    def consume_comment(self, comment):
        print(comment.body)

    def consume_submission(self, submission):
        print(submission.permalink)

    def consume_mod_log(self, mod_log):
        print(mod_log.target_permalink)
