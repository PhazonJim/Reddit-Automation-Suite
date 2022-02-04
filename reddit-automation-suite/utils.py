import yaml
import json
import os
import logging


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
        self._cache = None

    @property
    def config(self):
        if not self._config:
            self._config = self.load_config()
        return self._config

    @property
    def cache(self):
        if not self._cache:
            self._cache = self.load_cache()
        return self._cache

    def load_config(self):
        try:
            logging.debug(f"Loading config file from: {self.config_path}")
            return yaml.load(open(self.config_path).read(), Loader=yaml.FullLoader)
        except:
            logging.error(
                "'config.yaml' could not be located. Please ensure 'config.example' has been renamed"
            )
            exit()

    def load_cache(self):
        plugin_cache_dir = os.path.join(self.main_cache_dir, self.name)
        plugin_cache_file_path = os.path.join(plugin_cache_dir, "__cache.json")
        if not os.path.isdir(plugin_cache_dir):
            os.mkdir(plugin_cache_dir)
            return {}
        else:
            if not os.path.isfile(plugin_cache_file_path):
                return {}
            else:
                try:
                    with open(plugin_cache_file_path, "r") as fin:
                        return json.load(fin)
                except Exception as e:
                    print(e)

    def save_cache(self):
        plugin_cache_dir = os.path.join(self.main_cache_dir, self.name)
        plugin_cache_file_path = os.path.join(plugin_cache_dir, "__cache.json")
        with open(plugin_cache_file_path, "w") as fout:
            for chunk in json.JSONEncoder().iterencode(self.cache):
                fout.write(chunk)

    def consume_comment(self, comment):
        pass

    def consume_submission(self, submission):
        pass

    def consume_mod_log(self, mod_log):
        pass

    def consume_modmail(self, modmail):
        pass


def get_full_permalink(partial_permalink):
    return f"https://www.reddit.com{partial_permalink}"


def s_to_f(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')


def get_user_as_string(reddit_object):
    if reddit_object.author:
        return reddit_object.author.name
    else:
        return "[Unable to find user]"
