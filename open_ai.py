import openai
import os
import json
import pandas as pd

from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv
load_dotenv()

data = pd.read_csv("Datasets/SingleLabel.csv")

openai.api_key = os.getenv("OPENAI_KEY")

possible_moods = [
    "Sadness",
    "Tension",
    "Tenderness",
]

lemmatizer = WordNetLemmatizer()

random_state = 5
sample_size = 30
max_lyrics_length = 100

def lemmatize_word(word):
    tokens = word.split()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

data["lyrics"] = data["lyrics"].apply(lemmatize_word)
data["lyrics"] = data["lyrics"].apply(lambda lyrics: lyrics[:max_lyrics_length])

training_data = []

for index, row in data.iterrows():
    lyrics = row["lyrics"]
    mood_label = row["label"]
    example = {
        "input": f"Predict the mood for the following lyric: '{lyrics}'",
        "output": mood_label,
    }
    training_data.append(example)

def generate_mood_suggestion(input_text, model="gpt-3.5-turbo-16k"):
    prompt = f"Given the following list of possible moods: {', '.join(possible_moods)}, please suggest a suitable mood for the following text: '{input_text}'."
    conversation = [{"role": "user", "content": example["input"]} for example in training_data[:101]]
    conversation.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages = conversation,
        n=3,
        max_tokens=1000,
        temperature=0
    )
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