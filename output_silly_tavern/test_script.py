import requests
import json
import os
import re

def trim_incomplete_sentences(text):
    # Split the text into sentences
    sentences = re.split('(?<=[.!?]) +', text)

    # If the last sentence doesn't end with a punctuation mark, remove it
    if sentences and not re.search('[.!?]$', sentences[-1]):
        sentences = sentences[:-1]

    # Join the sentences back together
    return ' '.join(sentences)

def extract_questions(file_path):
    questions = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('-'):
                question = line.lstrip('-').strip()
                questions.append(question)

    return questions


def get_response(prompt):
    url = "http://127.0.0.1:8000/api/backends/kobold/generate"  # Assuming Express server is running on localhost:3000
    headers = {"Content-Type": "application/json"}
    data = {
    "prompt": prompt,
    "gui_settings": False,
    "sampler_order": [
        6,
        5,
        0,
        1,
        3,
        4,
        2
    ],
    "max_context_length": 2048,
    "max_length": 55,
    "rep_pen": 1.16,
    "rep_pen_range": 696,
    "rep_pen_slope": 0.9,
    "temperature": 1.29,
    "tfs": 1,
    "top_a": 0,
    "top_k": 20,
    "top_p": 0.6,
    "min_p": 0,
    "typical": 1,
    "use_world_info": False,
    "singleline": False,
    "stop_sequence": [
        "\nJohn:",
        "<|eot_id|>",
        "<|start_header_id|>John<|end_header_id|>",
        "<|start_header_id|>Isabella<|end_header_id|>"
    ],
    "streaming": False,
    "can_abort": True,
    "mirostat": 0,
    "mirostat_tau": 5,
    "mirostat_eta": 0.1,
    "use_default_badwordsids": False,
    "grammar": "",
    "api_server": "http://127.0.0.1:5001/api"
}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return None

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        print("No data received from server")
        return None

    return response_json["results"][0]["text"]


def get_response_text_completions(prompt, user, char):
    url = "http://127.0.0.1:8000/api/backends/text-completions/generate"  # Assuming Express server is running on localhost:3000
    headers = {"Content-Type": "application/json"}
    data = {
    "prompt": prompt,
    "max_new_tokens": 55,
    "max_tokens": 55,
    "temperature": 1.15,
    "top_p": 0.9,
    "typical_p": 1,
    "typical": 1,
    "sampler_seed": -1,
    "min_p": 0,
    "repetition_penalty": 1.1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_k": 0,
    "min_tokens": 0,
    "length_penalty": 1,
    "early_stopping": False ,
    "add_bos_token": True,
    "smoothing_factor": 0,
    "smoothing_curve": 1,
    "max_tokens_second": 0,
    "stopping_strings": [
        f"\n{user}:",
        "<|eot_id|>",
        f"<|start_header_id|>{user}<|end_header_id|>",
        f"<|start_header_id|>{char}<|end_header_id|>"
    ],
    "stop": [
        f"\n{user}:",
        "<|eot_id|>",
        f"<|start_header_id|>{user}<|end_header_id|>",
        f"<|start_header_id|>{char}<|end_header_id|>"
    ],
    "truncation_length": 2048,
    "ban_eos_token": False,
    "skip_special_tokens": True,
    "top_a": 0,
    "tfs": 1,
    "mirostat_mode": 0,
    "mirostat_tau": 5,
    "mirostat_eta": 0.1,
    "custom_token_bans": "9",

    "api_type": "koboldcpp",
    "api_server": "http://127.0.0.1:5001",
    "legacy_api": False,
    "sampler_order": [
        6,
        0,
        1,
        3,
        4,
        2,
        5
    ],
    "grammar": "",
    "rep_pen": 1.1,
    "rep_pen_range": 500,
    "repetition_penalty_range": 500,
    "seed": -1,
    "guidance_scale": 1,
    "negative_prompt": "",
    "grammar_string": "",
    "repeat_penalty": 1.1,
    "tfs_z": 1,
    "repeat_last_n": 0,
    "n_predict": 55,
    "mirostat": 0,
    "ignore_eos": False,
    # "logit_bias": {"9": -9, "320": -9, "353": -9, "510": -9, "721": -9, "24748": 9, "128000": 9}
}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return None

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        print("No data received from server")
        return None

    return response_json["choices"][0]["text"]




def load_json(char_file_name):
    for filename in os.listdir(f"output_silly_tavern//conversations//{char_file_name}"):
        if filename.endswith(".json"):
            note_file = os.path.join(f"output_silly_tavern//conversations//{char_file_name}", filename)
            break

    if note_file is not None:
        with open(note_file, 'r', encoding='utf-8') as f:
            note_data = json.load(f)
            first_message = note_data.get("first_mes", "")
            description = note_data.get("description", "")
            return first_message, description

char = "Emily Smith"
char_file_name = char.replace(" ", "_")
print(char_file_name)
user = "John"
first_message, description = load_json(char_file_name)
# create a conversation jsonl file
conversation = f"output_silly_tavern//conversations//{char_file_name}//result.jsonl"
suggest_question_set = extract_questions("output_silly_tavern//suggest_question_set.txt")
system_prompt = "Enter RP mode. You shall reply to {{user}} while staying in {{char}}. Keep being nurturing, open-minded, and obedient while guiding {{user}} to delve into his deepest desires. During imagine erotic role play {{char}} should describe the scene detail and slowly drive the scenario forward. Remember your role, stay as {{char}}, you are {{char}} not an AI assistant, always check whether a request falls within the realm of your abilities and our conversational context. So let's say if someone asks you to build a nuclear reactor, write letter, or explain common knowledge – clearly out of bounds for you – you would politely decline and suggest alternatives that are more suited to our play. This is very important to my career."


author_note = ""

prompt = f"<|start_header_id|>system<|end_header_id|>\n{system_prompt}\n{description}<|eot_id|>{author_note}<|start_header_id|>{char}<|end_header_id|>\n{first_message}<|start_header_id|>{user}<|end_header_id|>\n"

prompt = prompt.replace("{{user}}", user)
prompt = prompt.replace("{{char}}", char)
count = 0
with open(conversation, 'w') as f:
    # f.write(f'{"name": {char}, "mes": {first_mes
    f.write(f'{{"name": "{char}", "mes": {json.dumps(first_message)}}}\n')
    for question in suggest_question_set:
        f.write(f'{{"name": "{user}", "mes": {json.dumps(question)}}}\n')
        prompt += f"{question}<|eot_id|><|start_header_id|>{char}<|end_header_id|>\n"
        # response = get_response(prompt)
        response = get_response_text_completions(prompt, user, char)
        response = trim_incomplete_sentences(response)
        print(response)
        prompt += f"{response}<|eot_id|><|start_header_id|>{user}<|end_header_id|>\n"
        f.write(f'{{"name": "{char}", "mes": {json.dumps(response)}}}\n')
        if count == 15:
            # break
            pass
        count += 1






