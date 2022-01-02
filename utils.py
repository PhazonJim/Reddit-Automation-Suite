import yaml
import json 

CACHE_DIR = os.path.join(os.path.dirname(__file__), "/cache")

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
    try:
        with open(CACHE_FILE, "r") as fin:
            cache = json.load(fin)
    except Exception as e:
        print (e)
    return cache
    
def save_cache(file, data):
    with open(file, "w") as fout:
        for chunk in json.JSONEncoder().iterencode(data):
            fout.write(chunk)