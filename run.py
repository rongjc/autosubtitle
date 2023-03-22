from transcript import *
from translate import *

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Translate an SRT from a language to another using chatgpt.')
	parser.add_argument('--input', '-i', type=str, help='input SRT file,e.g. ./xxx.srt')
	parser.add_argument('--input_language', '-il', type=str, help='input SRT file language, e.g English')
	parser.add_argument('--output', '-o', type=str, help='output SRT file, e.g. ./xxx_translated.srt')
	parser.add_argument('--output_language', '-ol', type=str, help='output SRT file language, e.g. Japanese')
	parser.add_argument('--token', '-t', type=str, help='chatGPT api token')
	parser.add_argument('--chunk_size', '-n', type=str, default=1000, help='Chunk size of the API call')


	args = parser.parse_args()

	extract_audio(args.input)
	dirname = os.path.dirname(args.input)
	file_name = os.path.basename(args.input)
	file_basename = file_name.split('.')[0]
	mp3_path = os.path.join(dirname, file_basename+".mp3")
	srt_path = os.path.join(dirname, file_basename+".srt")
	extract_subtitle(mp3_path,'large-v2', args.input_language,srt_path)
	translate_gpt(srt_path,args.input_language,args.output,args.output_language, args.token, args.chunk_size)