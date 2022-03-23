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
        logging.info(
            f"New comment from {comment.author.name} ingested by plugin {self.name}: {comment.body}"
        )

    def consume_submission(self, submission):
        logging.info(
            f"New submission from {submission.author.name} ingested by plugin {self.name}: {submission.title}"
        )

    def consume_mod_log(self, mod_log):
        logging.info(
            f"New mod action from {mod_log._mod} ingested by plugin {self.name}: {mod_log.action}"
        )

    def consume_modmail(self, modmail):
        logging.info(
            f"New modmail from {modmail.owner} ingested by plugin {self.name}: {modmail.subject}"
        )
        print(vars(modmail))
