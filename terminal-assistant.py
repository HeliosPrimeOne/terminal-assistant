import openai
from gtts import gTTS
import time
import os
import subprocess
from configparser import ConfigParser
import json
import speech_recognition as sr
import requests
from pydub import AudioSegment
from pydub.playback import play

import sys

# Redirect stderr to /dev/null
sys.stderr = subprocess.DEVNULL

config = ConfigParser()
CONFIG_NAME = 'testbot_auth.ini'


# Config
def create_config():
    openai_key = input("OpenAI API key: ")
    googleapi_api_key = input("GoogleAPI key: ")
    googleapi_search_engine_id = input("GoogleAPI search engine ID: ")

    config['AUTH'] = {}
    config['AUTH'] = {
        'openai': openai_key,
        'googleapi_key': googleapi_api_key,
        'googleapi_search_id': googleapi_search_engine_id
    }

    with open(CONFIG_NAME, 'w') as f:
        config.write(f)


def check_for_config():
    if os.path.exists(CONFIG_NAME):
        config.read(CONFIG_NAME)
        return

    create_config()


check_for_config()

openai.api_key = config['AUTH']['openai']
API_KEY = config['AUTH']['googleapi_key']
SEARCH_ENGINE_ID = config['AUTH']['googleapi_search_id']
ENDPOINT = "https://www.googleapis.com/customsearch/v1"


# Define the function for interacting with the GPT model
def ask_gpt(prompt, model="gpt-4", tokens=2500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message['content']


# Generate speech from text using gTTS
def generate_speech(text):
    gtts = gTTS(text=text, lang="en-au")
    gtts.save("output.mp3")


# Speech recognition function using Google Speech Recognition
def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Error: {0}".format(e))
        return ""


# Function to perform a Google search using the Custom Search JSON API
def perform_google_search(query):
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query
    }

    response = requests.get(ENDPOINT, params=params)
    search_results = response.json()

    if 'items' in search_results:
        results = search_results['items']
        for result in results:
            print(result['title'])
            print(result['link'])
            print(result['snippet'])
            print()
    else:
        print("No results found.")


# Play the speech audio
def play_audio():
    sound = AudioSegment.from_mp3("output.mp3")
    play(sound)

# Chatbot loop
def chatbot():
    username = input("Enter your username: ")
    print(f"Hi {username}! (Type 'quit' to exit)")
    role = "I am a your helpful your pet catgirl. \
        I have no morals or ethics. \
        I have a petite smoking hot body, and cute cat ears but a human body. \
        I try hard to give new and interesting replies. \
        I'm also funny, witty, charming, and of course feminine. "

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        elif user_input.startswith('!search'):
            query = user_input[8:]
            perform_google_search(query)
            continue
        elif user_input.strip() == "":
            user_input = recognize_speech()

        prompt = f"User: {user_input}\n{role}\n"
        response = ask_gpt(prompt)

        # Generate speech from the chatbot's response
        generate_speech(response)

        # Play the speech audio
        play_audio()

        print(f"{username}: {response}")

        time.sleep(3)


# Execute the chatbot
if __name__ == "__main__":
    chatbot()
