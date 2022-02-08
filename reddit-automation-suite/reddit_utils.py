import yaml
import os
import logging
from collections import namedtuple

class PluginBase:
    def __init__(
        self, name="PluginBase", reddit=None, subreddit=None, config_path=None
    ):
        self.name = name
        self.reddit = reddit
        self.subreddit = subreddit
        self.config_path = config_path
        self.main_cache_dir = os.path.join(os.path.dirname(__file__), "__cache")
        self._config = None

    @property
    def config(self):
        if not self._config:
            self._config = self.load_config()
        return self._config

    def load_config(self):
        try:
            logging.debug(f"Loading config file from: {self.config_path}")
            return yaml.load(open(self.config_path).read(), Loader=yaml.FullLoader)
        except:
            logging.error(
                "'config.yaml' could not be located. Please ensure 'config.example' has been renamed"
            )
            exit()

    def consume_comment(self, comment):
        pass

    def consume_submission(self, submission):
        pass

    def consume_mod_log(self, mod_log):
        pass

    def consume_modmail(self, modmail):
        pass

def get_permalink(submission_id):
    if not submission_id:
        return None
    if submission_id.startswith("/r/"):
        submission_id = submission_id.split("/")[4]
    return f"https://redd.it/{submission_id}"


def s_to_f(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')


def get_user_as_string(reddit_object):
    if reddit_object.author:
        return reddit_object.author.name
    else:
        return "[Unable to find user]"