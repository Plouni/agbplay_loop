# agbplay_loop
Get loop points for .wav files exported with [agbplay.exe](https://github.com/ipatix/agbplay)

## Requirements
To download the songs, you'll need to have Python 3 installed with the following libraries:
* `numpy`
* `scipy`

## Project structure
.  
|_ agbplay/  
  |_ `agbplay.exe`  
  |_ `set_agbplay_maxloop_0.py`  
  |_ `set_agbplay_maxloop_1_and_rename_0.py`  
|_ input/  
|_ output/  
|_ `config.json`  
|_ `agbplay_loop.py`  
|_ `Readme.md`  

Folder details:
* `agbplay`: folder where optional python scripts are located. Check the `Optional` section for more details
* `input`: folder where .wav exported by agbplay.exe should be stored
* `output`: folder where the output .wav will be stored, as well as the json file that contains the loop points

## Usage
1) For each song that you want to loop, use `agbplay.exe` to export 2 wav files:
 - a `.wav` with no looping (set `"max-loops-export"` to 0 in agbplay's config). The filename of this .wav should end with `"_0.wav"`  
 - a `.wav` with 1 loop (set `"max-loops-export"` to 1 in agbplay's config)  

For example, if you're exporting a song called `'mymusic'` from agbplay:
 - `'mymusic_0.wav'` is the filename for the wav exported with no looping  
 - `'mymusic.wav'` is the filename for the wav exported with 1 loop 

2) Place all the exported .wav inside the `'input'` folder of this project.  

3) Run the python script `'agbplay_loop.py'`. This will compute the loop points for each pair and store them in a json file, inside the `'output'` folder. The output `.wav`, trimmed to the end loop point, will be located inside the same folder.

## (Optional) Setting up agbplay config
To make the agbplay.exe export faster, it is recommended to use the python scripts located in the `'agbplay'` folder, but some setup is needed for that:
- First, you'll need to edit agbplay's config and set `"wav-output-dir"` to the full path of this project's input folder ("C:/.../agbplay_loop/input")  
- Then, you'll need to open `'config.json'`, located at the root of this project, and set `"agbplay_config_path"` to the path of agbplay.exe's config (the one you've edited just above)  

After that, you're ready for the new agbplay process:
- Inside the `'agbplay/'` folder, run the script `'set_agbplay_maxloop_0.py'`. This will set "max-loops-export" to 0  
- Run `agbplay.exe` and export all the .wav that you want to loop  
- Run the script `'set_agbplay_maxloop_1_and_rename_0.py'`. This will set "max-loops-export" to 1 and rename all the wav produced earlier by adding `'_0'` at the end of the filename  
- Run `agbplay.exe` again to export the same wav files as before. That's all, you're now ready to run `'agbplay_loop.py'`
