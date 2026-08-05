import csv
import json

import requests
from pydantic import BaseModel

class SpellingBeeWord(BaseModel):
    level: int
    defintion: str
    pos: str
    word: str

def get_spelling_bee_word_details(word: str, level: int) -> SpellingBeeWord:
    word = word.split("|")[0]

    # try to get definitions for all of the words
    api_key = "7fbee7bc-3379-4f17-917e-c4755e2d7031"
    definition_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    full_def_url = definition_url.format(word=word, api_key=api_key)
    res = requests.get(full_def_url)
    if res.status_code != 200:
        raise ValueError(f"non 200 response {res.status_code}")

    details: list[dict] = res.json()

    if not len(details):
        raise ValueError(f"no definition for {word}")

    detail = details[0]

    backup_detail = None
    if len(details) > 1:
        backup_detail = details[1]

    if not isinstance(detail, dict):
        print(f"could not get definition for word: {word}")
        return None
        raise ValueError(f"getting some issue with word: {word}")

    short_defs = detail.get("shortdef", [])
    pos = detail.get("fl", None)
    if not pos:
        detail = backup_detail
        short_defs = detail.get("shortdef", [])
        pos = detail.get("fl", None)

        if not pos:
            raise ValueError(f"could not get pos for {word}")

    if not len(short_defs):
        raise ValueError(f"could not get definition for {word}")

    definition = short_defs[0]

    return SpellingBeeWord(
        defintion=definition,
        word=word,
        pos=pos,
        level=level
    )


level_1_words = []
level_2_words = []

with open('words/level_1.csv', 'r') as f:
    words = f.readlines()
    level_1_words = [word.strip() for word in words]

with open('words/level_2.csv', 'r') as f:
    words = f.readlines()
    level_2_words = [word.strip() for word in words]

level_2_spelling_bee_words: list[SpellingBeeWord] = [get_spelling_bee_word_details(word, 2) for word in level_2_words]
level_2_spelling_bee_words = [word for word in level_2_spelling_bee_words if word is not None]

with open('level_2_spelling_bee_words.csv', 'w', newline='') as csvfile:
    field_names = list(SpellingBeeWord.model_fields)
    writer = csv.DictWriter(csvfile, fieldnames=field_names)

    writer.writeheader()
    writer.writerows([word.model_dump() for word in level_2_spelling_bee_words])