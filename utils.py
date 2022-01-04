import yaml
import json 
import os

CACHE_DIR = os.path.join(os.path.dirname(__file__), "__cache")

class PluginBase:
    def __init__(self):
        self.name = "PluginBase"
        self.CACHE_DIR = ""
        self.CONFIG_FILE = ""
        self.cache = {}
        
    def load_config(self):
        try:
            print(f"Loading config file from: {self.CONFIG_FILE}")
            return yaml.load(open(self.CONFIG_FILE).read(), Loader=yaml.FullLoader)
        except:
            print("'config.yaml' could not be located. Please ensure 'config.example' has been renamed")
            exit()

    def load_cache(self):
        cache = {}
        PLUGIN_CACHE_DIR = os.path.join(CACHE_DIR, self.name)
        PLUGIN_CACHE_FILE_PATH = os.path.join(PLUGIN_CACHE_DIR, "__cache.json")
        if not os.path.isdir(PLUGIN_CACHE_DIR):
            os.mkdir(PLUGIN_CACHE_DIR)
            return cache
        else:
            if not os.path.isfile(PLUGIN_CACHE_FILE_PATH):
                return cache
            else:
                try:
                    with open(PLUGIN_CACHE_FILE_PATH, "r") as fin:
                        cache = json.load(fin)
                except Exception as e:
                    print (e)
                return cache

    def save_cache(self):
        PLUGIN_CACHE_DIR = os.path.join(CACHE_DIR, self.name)
        PLUGIN_CACHE_FILE_PATH = os.path.join(PLUGIN_CACHE_DIR, "__cache.json")
        with open(PLUGIN_CACHE_FILE_PATH, "w") as fout:
            for chunk in json.JSONEncoder().iterencode(self.cache):
                fout.write(chunk)