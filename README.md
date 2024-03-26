# agbplay_loop
Get loop points from .wav files exported with [agbplay.exe](https://github.com/ipatix/agbplay)

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
* agbplay: folder where optional python scripts are located. Use these to export and rename the wav from agbplay.exe more quickly
* input: folder where .wav exported by agbplay.exe should be stored
* output: folder where output .wav will be stored, as well as the json file that will contain the start_loop points

Please also keep the config and the python script at the root of this project or it won't work.

## Usage
1) For each song you want to loop, use `agbplay.exe` to export it two times:
 - one time with no looping (set `"max-loops-export"` to 0 in the agbplay's config), the filename of this .wav should end with `"_0.wav"`  
 - the second time with 1 looping (set `"max-loops-export"` to 1 in the agbplay's config)  

For example, if you're exporting a song called `'mymusic'` from agbplay:
 - `'mymusic_0.wav'` is the filename for the wav exported with no looping  
 - `'mymusic.wav'` is the filename for the wav exported with 1 looping  

2) Place all the exported .wav in the `'input'` folder of this project.  

3) Run the python script `'agbplay_loop.py'`. This will compute the loop points for each pair of wav and export the trimmed `.wav` to the `'output'` folder. A json that contains the start loop for each .wav will also be produced inside the `'output'` folder. 

## (Optional) Setting up agbplay config
To make the agbplay export faster, it is recommended to use the python scripts located in the `'agbplay'` folder, but some setup is needed for that.
- First, you'll need to edit your agbplay config and set `"wav-output-dir"` to the full path of this project's input folder ("C:/.../agbplay_loop/input")  
- Then, you'll need to open the `'config.json'` located at the root of this project and set `"agbplay_config_path"` to the path of agbplay.exe's config (the one you've edited just above)  

After that, you're ready for the new agbplay process:
- Inside the `'agbplay/'` folder, run the script `'set_agbplay_maxloop_0.py'`. This will set "max-loops-export" to 0  
- Run `agbplay.exe` to export all the .wav that you want to loop  
- Run the script `'set_agbplay_maxloop_1_and_rename_0.py'`. This will set "max-loops-export" to 1 and rename all the wav produced earlier by adding `'_0'` at the end of the filename  
- Run `agbplay.exe` again to export the same wav files as before. Now, you have all the wave needed to run `'agbplay_loop.py'`
