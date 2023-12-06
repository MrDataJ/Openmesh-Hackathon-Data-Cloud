import json

def load_config(filename):
    with open(f'config/{filename}') as config_file:
        return json.load(config_file)