import json

import requests

level_1_words = []
level_2_words = []

with open('words/level_1.csv', 'r') as f:
    words = f.readlines()
    level_1_words = [word.strip() for word in words]

with open('words/level_2.csv', 'r') as f:
    words = f.readlines()
    level_2_words = [word.strip() for word in words]

all_words = [*level_1_words, *level_2_words]

# try to get definitions for all of the words
api_key = "7fbee7bc-3379-4f17-917e-c4755e2d7031"
definition_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
for word in all_words:
    if word != "peeve":
        continue

    full_def_url = definition_url.format(word=word, api_key=api_key)
    res = requests.get(full_def_url)
    def_obj = res.json()

    with open(f"def_obj_{word}.json", 'w') as f:
        json.dump(def_obj, f)
