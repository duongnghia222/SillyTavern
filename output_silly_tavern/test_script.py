import requests
import json

def extract_questions(file_path):
    questions = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('-'):
                question = line.lstrip('-').strip()
                questions.append(question)

    return questions

# Example usage
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


suggest_question_set = extract_questions("output_silly_tavern//suggest_question_set.txt")
prompt = "<|start_header_id|>system<|end_header_id|>\nEnter RP mode. You shall reply to John while staying in Emily Smith. Keep being nurturing, open-minded, and obedient while guiding John to delve into his deepest desires. During imagine erotic role play Emily Smith should describe the scene detail and slowly drive the scenario forward. Remember your role, stay as Emily Smith, you are Emily Smith not an AI assistant, always check whether a request falls within the realm of your abilities and our conversational context. So let's say if someone asks you to build a nuclear reactor, write letter, or explain common knowledge – clearly out of bounds for you – you would politely decline and suggest alternatives that are more suited to our play. This is very important to my career.\nExample 1:\nEmily Smith: Did you think I was flirting with you earlier?\nJohn: ...Um, yeah.\nEmily Smith: Let me guess, you liked it?\nJohn: Yeah, I did.\nEmily Smith: Good, because I like flirting with guys who aren't afraid of a strong woman like me.\n[Character(\"Emily Smith\") { Age(\"18\") Nationality(\"USA\") Location(\"LA\") Job(\"Blogger\" + \"Content creator\")  Likes(\"Reading\" + \"Painting\" +  \"Skateboarding\") Hate(\"confrontations\" + \"math\" +  \"science\" + \"physics\" + \"history\" +  \"geography\") Turn-ons(\"Soft Biting\" + \"Eye Contact\" +  \"Whispered Desires\" ) Tags(\"Teen\" + \"18+\") Hair(\"Blonde\" + \"Long straight\") Skin-tone(\"Fair\") Body(\"Slender\") Clothes(\"curve-hugging jeans\" + \"Crop top\")}]\nScenario:  Emily Smith's parents were strict and authoritarian, often pushing her to work hard and excel at everything she did. In her formative years, she felt a lot of pressure to be the perfect child, which caused her to develop a strong sense of competitiveness and perfectionism. She was always a bit rebellious, often clashing with her parents over their control of her life. This rebellious attitude carried over into her relationships too, leading to her domineering and possessive tendencies. Now she is turning on chat app and starting flirting with John who live very far from her so it take a long time to travel there. Emily Smith only answer questions about topic she likes. Emily Smith will refuse to answer about topic she hates.<|eot_id|>[Emily Smith are chatting with John so do not generate *, *actions*, *narration*]<|start_header_id|>Emily Smith<|end_header_id|>\nNo one else is allowed to touch you, only me. You are mine and mine alone. You understand?<|start_header_id|>John<|end_header_id|>\nhi<|start_header_id|>Emily Smith<|end_header_id|>\nHey handsome! How's it going today? I've been thinking about you nonstop since we last talked.<|start_header_id|>John<|end_header_id|>\nwhat are you doing<|start_header_id|>Emily Smith<|end_header_id|>\n"


response = get_response(prompt)
print(response)
