import os
import json

# Loading config variables
with open('../config.json') as f:
    config = json.load(f)
    
agbplay_config_path = config['agbplay_config_path']

# Loading input folder
input_folder = config['input_folder']

with open(agbplay_config_path, "r+", encoding='latin-1') as f:
    txt = f.read()
    txt = txt.replace('"max-loops-export" : 0,', '"max-loops-export" : 1,')
    f.seek(0)
    f.truncate(0)
    f.write(txt)
    
# Change back to current_path
os.chdir('..')

out_agb_folder = input_folder
for file in os.listdir(out_agb_folder):
    if '.wav' not in file or '_1' in file:
        continue
        
    file_new = file.replace(".wav", "_0.wav")
    os.rename(out_agb_folder + file, out_agb_folder + file_new)