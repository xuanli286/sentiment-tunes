import openai
import os
import json
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

data = pd.read_csv("Datasets/MultiLabel.csv")

openai.api_key = os.getenv("OPENAI_KEY")

possible_moods = [
    "amazement",
    "calmness",
    "joyful activation",
    "solemnity",
    "nostalgia",
    "power",
    "tenderness",
    "tension",
    "sadness"
]

training_data = []
for index, row in data.iterrows():
    title = row["title"]
    mood_label = row["labels"]
    example = {
        "input": f"Predict the mood for the following lyric: '{title}'",
        "output": mood_label,
    }
    training_data.append(example)

def generate_mood_suggestion(input_text, model="gpt-3.5-turbo-16k"):
    prompt = f"Given the following list of possible moods: {', '.join(possible_moods)}, please suggest a suitable mood for the following text: '{input_text}'."
    conversation = [{"role": "user", "content": example["input"]} for example in training_data[:500]]
    conversation.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages = conversation,
        n=8,
        temperature=0
    )
    prompt = prompt.format(text=input_text)
    suggested_mood = response['choices'][0]['message']['content']
    for mood in possible_moods:
        if mood in suggested_mood:
            return mood

def string_to_json(text: str):
    text = text.replace("`", "")
    text = text.replace("json", "")
    return json.loads(text)

if __name__ == "__main__":
    print(generate_mood_suggestion("I got f grade for my exammmm"))