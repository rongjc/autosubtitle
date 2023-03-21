import os
import subprocess
import whisper
import time
from urllib.parse import quote_plus
from pathlib import Path
import sys
import torch



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
	os.system(f'ffmpeg -i {file_name} -f mp3 -ab 192000 -vn {file_basename}.mp3')
	toc = time.time()
	print(f'Time for extract_audio: {toc-tic}s')
	pass

def extract_subtitle(filepath, model_size, language):
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
	with open(Path(dirname) / (file_basename + ".srt"), "w", encoding="utf-8") as srt:
		writer = WriteSRT(dirname)
		writer.write_result(result, srt)

# extract_audio("./mx.mp4")
extract_subtitle("./mx.mp3",'large-v2', 'Japanese')
# print('加载模型 Loading model...')
# model = whisper.load_model(model_size)

# #Transcribe
# tic = time.time()
# print('识别中 Transcribe in progress...')
# result = model.transcribe(audio = f'{file_name}', language= language, verbose=False)

# #Anonymous usage data for stats
# #Comment out this block if you do not want send your data
# try: 
#   requests.get(f'https://api.callmebot.com/whatsapp.php?phone=61402628080&text={file_name}+N46Whisper&apikey=8080872')
# except Exception as e:
#   pass

# #Time comsumed
# toc = time.time()
# print('识别完毕 Done')
# print(f'Time consumpution {toc-tic}s')

# #Write SRT file
# from whisper.utils import WriteSRT
# with open(Path(output_dir) / (file_basename + ".srt"), "w", encoding="utf-8") as srt:
#     writer = WriteSRT(output_dir)
#     writer.write_result(result, srt)
# #Convert SRT to ASS

# from srt2ass import srt2ass
# assSub = srt2ass(file_basename + ".srt", sub_style, is_split,split_method)
# print('ASS subtitle saved as: ' + assSub)
# files.download(assSub)
# # os.remove(file_basename + ".srt")
# torch.cuda.empty_cache()
# print('字幕生成完毕 All done!')

# torch.cuda.empty_cache()