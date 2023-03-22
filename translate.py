import openai
import argparse
import time
import tiktoken
import re

# check number of tokens of a message
def num_tokens_from_messages(message, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = len(encoding.encode(message))
        return num_tokens
    else:
        raise NotImplementedError(f"""error.""")

# group messages together 
def group_chunks(chunks, ntokens, max_len=1000):
    """
    Group very short chunks, to form approximately a page long chunks.
    """
    batches = []
    cur_batch = ""
    cur_tokens = 0

    # iterate over chunks, and group the short ones together
    for chunk, ntoken in zip(chunks, ntokens):
        # print(ntoken)
        # notken = num_tokens_from_messages(chunk)
        cur_tokens += ntoken + 2  # +2 for the newlines between chunks

        # if adding this chunk would exceed the max length, finalize the current batch and start a new one
        if ntoken + cur_tokens > max_len:
            batches.append(cur_batch)
            cur_batch = chunk
            cur_tokens = 0
        else:
            cur_batch += "\n\n" + chunk
            # cur_batch += chunk
    batches.append(cur_batch)
    return batches

def write_srt_file(filename, subtitles):
    with open(filename, 'w') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['number']}\n{subtitle['start_time']} --> {subtitle['end_time']}\n{subtitle['text']}\n\n")

def parse_srt_data(srt_data):
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n\n'
    matches = re.findall(pattern, srt_data, re.DOTALL)
    subtitles = []
    for match in matches:
        subtitle = {
            'number': int(match[0]),
            'start_time': match[1],
            'end_time': match[2],
            'text': match[3].strip()
        }
        subtitles.append(subtitle)
    return subtitles

def translate(text,input_language,output_language):
    
    prompt_text = f"""
Task: Translate the text from {input_language} to {output_language}. For each chunk, the first row is a number and the second row is a text. Only translate the text part and keep the format
Text to translate:
{text}"""
    print(prompt_text)
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    # english prompt here to save tokens
                    # "content": f"This is a SRT file, Please translate the Japanese text to Chinese. The files are numbered, so please keep the format and numbering. Here is the srt file:\n\n `{text}` ",
                    "content": prompt_text
                }
            ],
        )
        t_text = (
            completion["choices"][0]
            .get("message")
            .get("content")
            .encode("utf8")
            .decode()
        )
        # format the translated text, the original text is eg: "\n\n['\\n柠檬\\n\\n', '梶井基次郎']", we need the
        # element in the list, not the \n \n
        
        try:
            t_text = ast.literal_eval(t_text)
        except Exception:
            # some ["\n"] not literal_eval, not influence the result
            pass
        # openai has a time limit for api  Limit: 20 / min
        time.sleep(3)
    except Exception as e:
        print(str(e), "will sleep 60 seconds")
        # TIME LIMIT for open api please pay
        time.sleep(60)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
        )
        t_text = (
            completion["choices"][0]
            .get("message")
            .get("content")
            .encode("utf8")
            .decode()
        )
        t_text = t_text.strip("\n")
        try:
            t_text = ast.literal_eval(t_text)
        except Exception:
            pass
    print(t_text)
    return t_text

def translate_gpt(input, input_language, output, output_language, api_key, chunk_size):
    
    openai.api_key = api_key
    file = input
    file_out = output
    print(file)
    with open(file, "r") as f:
        text = f.read()

    subtitles = parse_srt_data(text)
    ntokens = []
    chunks = []
    for subtitle in subtitles:
        chunk = str(subtitle['number'])+'\n' + subtitle['text']
        chunks.append(chunk)
        ntokens.append(num_tokens_from_messages(chunk))
    
    chunks = group_chunks(chunks, ntokens,chunk_size)
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(str(i+1) + " / " + str(len(chunks)))
        translated_chunks.append(translate(chunk,input_language, output_language)+"\n")
    
    # join the chunks together
    result = '\n'.join(translated_chunks)
    data = {}
    pattern = r'(\d+)\n(.+?)\n'
    matches = re.findall(pattern, result, re.DOTALL)
    for match in matches:
        data[str(match[0])] = match[1]
    
    for subtitle in subtitles:
        if str(subtitle['number']) in data:
            subtitle['text'] = data[str(subtitle['number']) ]
    
    write_srt_file(output, subtitles)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate an SRT from a language to another using chatgpt.')
    parser.add_argument('--input', '-i', type=str, help='input SRT file,e.g. ./xxx.srt')
    parser.add_argument('--input_language', '-il', type=str, help='input SRT file language, e.g English')
    parser.add_argument('--output', '-o', type=str, help='output SRT file, e.g. ./xxx_translated.srt')
    parser.add_argument('--output_language', '-ol', type=str, help='output SRT file language, e.g. Japanese')
    parser.add_argument('--token', '-t', type=str, help='chatGPT api token')
    parser.add_argument('--chunk_size', '-n', type=str, default=1000, help='Chunk size of the API call')

    args = parser.parse_args()
    translate_gpt(args.input,args.input_language,args.output,args.output_language, args.token, args.chunk_size)