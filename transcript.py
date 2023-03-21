import os
import subprocess
import whisper
import time
from urllib.parse import quote_plus
from pathlib import Path
import sys
import torch
import argparse


# file_type = "audio"  # @param ["audio","video"]

# model_size = "large-v2"  # @param ["base","small","medium", "large-v1","large-v2"]
# language = "japanese"  # @param {type:"string"}
# is_split = "No"  # @param ["No","Yes"]
# split_method = "Modest"  # @param ["Modest","Aggressive"]
# sub_style = "default"  # @param ["default", "ikedaCN", "kaedeCN","sugawaraCN","taniguchiCN","asukaCN"]

# compression_ratio_threshold = 2.4 # @param {type:"number"}
# no_speech_threshold = 0.6 # @param {type:"number"}
# logprob_threshold = -1.0 # @param {type:"number"}
# condition_on_previous_text = "True" # @param ["True", "False"]



def extract_audio(filepath):
	print('Extracting audio from video file...')
	tic = time.time()
	dirname = os.path.dirname(filepath)
	file_name = os.path.basename(filepath)
	file_basename = file_name.split('.')[0]
	os.system(f'ffmpeg -i {filepath} -f mp3 -ab 192000 -vn {file_basename}.mp3')
	toc = time.time()
	print(f'Time for extract_audio: {toc-tic}s')
	pass

def extract_subtitle(filepath, model_size, language,srt_path):
	tic = time.time()
	print('Loading model...')
	model = whisper.load_model(model_size)
	
	dirname = os.path.dirname(filepath)
	file_name = os.path.basename(filepath)
	file_basename = file_name.split('.')[0]

	print('Transcribe in progress...')
	result = model.transcribe(audio = f'{filepath}', language= language, verbose=False)
	print('Done')
	toc = time.time()
	print(f'Time for extract_subtitle: {toc-tic}s')
	file_basename = file_name.split('.')[0]
	from whisper.utils import WriteSRT
	with open(srt_path, "w", encoding="utf-8") as srt:
		writer = WriteSRT(dirname)
		writer.write_result(result, srt)

parser = argparse.ArgumentParser(description='Extract the audio and auto generate SRT file of a given video.')
parser.add_argument('--input', '-i', type=str, help='input video file path, for example ./xxx.mp4')
parser.add_argument('--language', '-l', type=str, help='main language of the video, for example english')
parser.add_argument('--output', '-o', type=str, help='output SRT file path, for example ./xxx.srt')

args = parser.parse_args()
# print('Input file:', args.input)
# print('language:', args.language)
extract_audio(args.input)
file_name = os.path.basename(args.input)
file_basename = file_name.split('.')[0]+".mp3"
extract_subtitle(file_name.split('.')[0]+".mp3",'large-v2', args.language,args.output)