"""
This module provides a naughty assistant using OpenAI's GPT-4 model.
"""

import time
import os
from configparser import ConfigParser
import speech_recognition as sr
import requests
from pydub import AudioSegment
from pydub.playback import play

import openai
from gtts import gTTS

config = ConfigParser()
CONFIG_NAME = 'ta_auth.ini'
MORALITY_LEVEL = 'high'  # Default value


def create_config():
    """
    Function to create a configuration file.
    """
    openai_key = input("OpenAI API key: ")
    googleapi_api_key = input("GoogleAPI key: ")
    googleapi_search_engine_id = input("GoogleAPI search engine ID: ")
    morality_level = input("Morality Level (high/low): ")

    config['AUTH'] = {
        'openai': openai_key,
        'googleapi_key': googleapi_api_key,
        'googleapi_search_id': googleapi_search_engine_id
    }
    config['SETTINGS'] = {
        'morality_level': morality_level
    }

    with open(CONFIG_NAME, 'w', encoding='utf-8') as config_file:
        config.write(config_file)


def check_for_config():

    """
    Function to check for a configuration file.
    """
    # pylint: disable=global-statement
    global MORALITY_LEVEL
    if os.path.exists(CONFIG_NAME):
        config.read(CONFIG_NAME)
        MORALITY_LEVEL = config['SETTINGS'].get('morality_level', 'high')
        return

    create_config()


check_for_config()

openai.api_key = config['AUTH']['openai']
API_KEY = config['AUTH']['googleapi_key']
SEARCH_ENGINE_ID = config['AUTH']['googleapi_search_id']
ENDPOINT = "https://www.googleapis.com/customsearch/v1"


def ask_gpt(prompt, model="gpt-4", tokens=2500):
    """
    Function to interact with the GPT model.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "I am your helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    if MORALITY_LEVEL == 'low':
        return 'Why dont you whip it out so I have something \
                to play with while we chat'
    return response.choices[0].message['content']


def generate_speech(text):
    """
    Function to generate speech from text using gTTS.
    """
    gtts = gTTS(text=text, lang="en-au")
    gtts.save("output.mp3")


def recognize_speech():
    """
    Function to recognize speech using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak:")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as error:
        print(f"Error: {error}")
        return ""


def perform_google_search(query):
    """
    Function to perform a Google search using the Custom Search JSON API.
    """
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query
    }

    response = requests.get(ENDPOINT, params=params, timeout=5)
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


def play_audio():
    """
    Function to play the speech audio.
    """
    sound = AudioSegment.from_mp3("output.mp3")
    play(sound)


def chatbot():
    """
    Main chatbot loop.
    """
    username = input("Enter your username: ")
    print(f"Hi {username}! (Type '!search' to query Google Search, \
        Press 'Enter' to respond with text input, \
        Press 'Shift+Enter' to respond with voice input, Type 'quit' to exit)")
    role = "I am a your helpful assistant. \
        I try hard to give new and interesting replies. \
        I'm also funny, witty, charming, and a great programmer. "

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        if user_input.startswith('!search'):
            query = user_input[8:]
            perform_google_search(query)
            continue
        if user_input.strip() == "":
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
