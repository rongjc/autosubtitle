import openai
# from transformers import GPT2Tokenizer
import time
import tiktoken

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
    batches.append(cur_batch)
    return batches

def translate(text):
        
        prompt_text = f"This is a SRT file, Please translate the Japanese text to Chinese. The files are numbered, so please keep the format and numbering. Here is the srt file:\n\n `{text}` ",
        print(text)
        # openai.api_key = self.key
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        # english prompt here to save tokens
                        "content": f"This is a SRT file, Please translate the Japanese text to Chinese. The files are numbered, so please keep the format and numbering. Here is the srt file:\n\n `{text}` ",
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
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": f"This is a SRT file, Please translate the Japanese text to Chinese. The files are numbered, so please keep the format and numbering. Here is the srt file:\n\n `{text}` ",
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

def run(input, output, api_key, chunk_size=500):
	
	openai.api_key = api_key
	file = input
	file_out = output
	
	with open(file, "r") as f:
	    text = f.read()

	chunks = text.split('\n\n')
	ntokens = []
	for chunk in chunks:
	    ntokens.append(num_tokens_from_messages(chunk))
	
	chunks = group_chunks(chunks, ntokens,chunk_size)
	


	dest_language = "Chinese"

	translated_chunks = []
	for i, chunk in enumerate(chunks):
	    print(str(i+1) + " / " + str(len(chunks)))
	    # print(chunk)
	    # print(num_tokens_from_messages(chunk))
	    # translate each chunk
	    # translated_chunks.append(translate_chunk(chunk, engine='text-davinci-003', dest_language=dest_language))
	    translated_chunks.append(translate(chunk))

	    # with open(i, "w") as f:
	    #     text = f.write(temp)
	    #     f.close()

	# join the chunks together
	result = '\n'.join(translated_chunks)

	# save the final result
	with open(file_out, "w") as f:
	    text = f.write(result)
	    f.close()


run('./mx.srt', './mx_chinese.srt', "")