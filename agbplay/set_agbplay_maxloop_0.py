import os
import json

# Loading config variables
with open('../config.json') as f:
    config = json.load(f)
    
agbplay_config_path = config['agbplay_config_path']

# Loading default normalisation level
default_normalization_level = config['default_normalization_level']

with open(agbplay_config_path, "r+") as f:
    txt = f.read()
    txt = txt.replace('"max-loops-export" : 1,', '"max-loops-export" : 0,')
    f.seek(0)
    f.truncate(0)
    f.write(txt)