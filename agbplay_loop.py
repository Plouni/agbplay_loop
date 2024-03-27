import os
import sys
import json
import wave
import array
import numpy as np
from scipy.io.wavfile import read, write
import warnings
warnings.filterwarnings("ignore")


# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading amount of s to trim to skip fadeout
trim_end_s = config['trim_end_s']

# Loading input folder
input_folder = config['input_folder']

# Loading output folder
output_path = config['output_path']

# Loading filename of json that will store looping data
output_start_loop_file = config['output_start_loop_file']

# Loading if valid .wav should be deleted after being converted to .pcm 
delete_valid_wav_after_pcm_generated = config['delete_valid_wav_after_pcm_generated']

current_path = os.getcwd().replace('\\', '/') + '/'


def float_to_int16_wav(input, output):
    rate, data  = read(input)
    data /=1.414
    data *= 32767
    write(output, rate, data.astype(np.int16))
    
    if delete_valid_wav_after_pcm_generated:
        os.remove(input)


def trim_wav(file1, output):
    """
    Check if song is mono and convert it to stereo if that's the case
    
    :file1: input file
    :output: name of pcm output file
    """
    ifile = wave.open("input/" + file1)
    (_, _, _, nframes_1, _, _) = ifile.getparams()
    
    file0 = file1.split(".wav")[0] + '_0.wav'
    ifile = wave.open("input/" + file0)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
    ifile.close()
    
    start_loop = nframes - (nframes_1 - nframes)
    framerate_trim = framerate*trim_end_s
    
    # print(nframes_1, nframes, start_loop)
    # print(file1, nchannels, framerate, start_loop-framerate_trim)

    
    ifile = wave.open("input/" + file0, 'rb')
    frames_limit = ifile.readframes( nframes - framerate_trim )
    ifile.close()

    ofile = wave.open(output, 'w')
    ofile.setparams((2, sampwidth, framerate, nframes - framerate_trim, comptype, compname))
    ofile.writeframes( frames_limit )
    ofile.close()
    
    return start_loop - framerate_trim, nframes - framerate_trim    


def create_folder(path):
    """
    Create folder if does not exist
    
    :path: path of directory to create
    """
    if not os.path.exists(path):
        os.mkdir(path)

# Creating output and input folder
create_folder(input_folder)
create_folder(output_path)


def main():
    print("# This script will compute the loop points for the .wav inside the 'input' folder #\n")

    # Clean Input wav filename
    for file in os.listdir(input_folder):
        if '.wav' not in file or ' - ' not in file:
            continue
            
        file_new = file.split(' - ')[1]
        file_new = file_new.replace('', '').replace(' ', '_').replace('&', '')
        os.rename(input_folder + file, input_folder + file_new)

    # List of .wav inside input folder
    wav_files = [wav for wav in os.listdir(input_folder) if ".wav" in wav and "_0." not in wav]
      

    if len(wav_files) == 0:
        input("No .wav files found inside folder {}. Press enter to finish.\n".format(input_folder))

    else:
        tracks = {}
    
        for wav in wav_files:
            # Remove spaces for output file
            if ' ' in wav:
                wav_clean = wav.replace(' ', '_')
            else:
                wav_clean = wav
                
            wav_no_ext = wav.split('.wav')[0]
            wav_0 = wav_no_ext + "_0.wav"
            
            # Skipping if 0 loop not found
            if wav_0 not in os.listdir(input_folder):
                print("0 loop version not found! Skipping: {}".format(wav))
                continue
            
            # name of modified file, cleaned by sox
            wav_modif = "modified_" + wav_clean
            wav_0_modif = "modified_" + wav_clean.split('.wav')[0] + "_0.wav"
            
            # Convert wav 16 using sox and remove input file          
            float_to_int16_wav(input_folder+wav, input_folder + wav_modif)
            float_to_int16_wav(input_folder+wav_0, input_folder + wav_0_modif)
            
            # Compute start/end loop and trim wav
            start_loop, end_loop = trim_wav(wav_modif, output_path + wav_clean)
            
            # start_loop is negative if sound is short (like a sound). In that case we skip it and rename it
            if start_loop < 0:
                print("skipped sound: {}".format(wav))
                os.remove(input_folder+wav_0_modif)
                os.rename(input_folder + wav_modif, input_folder+wav_modif.replace("modified_", "sound_"))
                continue
            
            
            # Store data in tracks dict
            tracks[wav_no_ext] = {"start_loop": start_loop, "end_loop": end_loop}
            
            # Remove modified file output by sox
            if delete_valid_wav_after_pcm_generated:
                os.remove(input_folder+wav_modif)
                os.remove(input_folder+wav_0_modif)
        
        # Loading config variables
        with open(output_path + '/' + output_start_loop_file, "w+") as f:
            json.dump(tracks, f, indent=4)

        input("Process complete! Loop points and trimmed .wav available in folder '{}'. Press enter to finish.\n".format(output_path))


if __name__ == "__main__":
    main()