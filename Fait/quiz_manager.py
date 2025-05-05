import json
import random

def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_random_question(questions):
    return random.choice(questions)
