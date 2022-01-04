import yaml
import json 
import os

CACHE_DIR = os.path.join(os.path.dirname(__file__), "__cache")

class PluginBase:
    def __init__(self):
        pass
        
def load_config(file):
    try:
        print(f"Loading config file from: {file}")
        return yaml.load(open(file).read(), Loader=yaml.FullLoader)
    except:
        print("'config.yaml' could not be located. Please ensure 'config.example' has been renamed")
        exit()

def load_cache(plugin_name):
    cache = {}
    PLUGIN_CACHE_DIR = os.path.join(CACHE_DIR, plugin_name)
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

def save_cache(file, data):
    with open(file, "w") as fout:
        for chunk in json.JSONEncoder().iterencode(data):
            fout.write(chunk)