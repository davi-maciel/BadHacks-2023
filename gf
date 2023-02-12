#!/usr/bin/env python3

import sys
import os
import openai
import json
import typer
from rich import print
import re

# Initial prompt to our conversation with GPT3
global prompt
prompt = "Imitate my girlfriend. She is Hatsune Miku. If I say goodbye, finish the conversation and in the next line say EndOfConversation\n\nYou: Hey, I love you.\nGirlfriend: Thank you, I love you too darling!"

# Default to Girlfriend
global xfriend
xfriend = "Girlfriend: "

def debug():
    print(prompt)

def print_help():
    print("""usage: girlfriend [-h] [-n NAME] [-k KEY]

CLI Girlfriend

options:
  -h, --help                       show this help message and exit
  -p STRING, --personality STRING  Replaces the default girlfriend personality
  -k KEY, --key KEY                Provides the OpenAI key
  -b, --boyfriend                  Provides the OpenAI key""")

# Remove weird blank spaces from beginning and end of response
def filter_blank_spaces(string):
    string = re.sub("^\s*", "", string, flags=re.IGNORECASE)
    string = re.sub("\s*$", "", string, flags=re.IGNORECASE)
    return string

# Get response from GPT3 given the full history convesration
def get_response(fullPrompt):
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullPrompt,
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[xfriend, "You:"]
    )
    response = data["choices"][0]["text"];
    response = filter_blank_spaces(response)
    return response

# Find emotion related to the response to change the image
def get_emotion(response):
    emotionPrompt = "Emotions available: Laughing, Blushed, Wink, Agree, Angry, Confident, Crying, Neutral, Sad\n\n" + "Sentence: I don't like you!\nEmotion: Angry\nSentence: " + response + "\nEmotion: "
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=emotionPrompt,
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    emotionResponse = data["choices"][0]["text"];
    emotionResponse = filter_blank_spaces(emotionResponse)
    return emotionResponse

# Format the conversation
def talk(userInput):
    try:
        global prompt
        prompt = prompt + "\nYou: " + userInput + "\n" + xfriend

        response = get_response(prompt)
        emotion = get_emotion(response)
        prompt = prompt + response;

        if (re.search("EndOfConversation", response, flags=re.IGNORECASE)):
            response = re.sub("EndOfConversation.*", "", response, flags=re.IGNORECASE)
            if len(response) == 0:
                print("[magenta]" + xfriend + "[/magenta]" + "Love you, bye!")
            else:
                print("[magenta]" + xfriend + "[/magenta]" + response)
            os.sys.exit()

        return "[magenta]" + xfriend + "[/magenta]" + response

    except openai.error.RateLimitError as e:
        return "Rate limit exceeded: " + e
# While loop
def REPL():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    while True:
        print("[blue]You: [/blue]", end='')
        userInput = input()
        if userInput == "exit" or userInput == "quit":
            break
        print(talk(userInput))

# Main function
if __name__ == "__main__":
    # No arguments
    if len(sys.argv) == 1:
        REPL()
    # Flag without arguments
    elif len(sys.argv) == 2:
        # Boyfriend instead of girlfriend
        if sys.argv[1] == "-b" or sys.argv[1] == "--boyfriend":
            prompt = "Imitate my boyfriend. If I say goodbye, finish the conversation and in the next line say EndOfConversation\n\nYou: Hey, I love you.\nBoyfriend: Thank you, I love you too darling!"
            xfriend = "Boyfriend: "
            REPL()
        # Help message
        else:
            print_help()
    # Flag with arguments
    elif len(sys.argv) == 3:
        # API Key
        if sys.argv[1] == "-k" or sys.argv[1] == "--key":
            putenv("OPENAI_API_KEY", sys.argv[2])
        # Change personality
        elif sys.argv[1] == "-p" or sys.argv[1] == "--personality":
            prompt = "Imitate my girlfriend. She is " + sys.argv[2] + ". If I say goodbye, finish the conversation and in the next line say EndOfConversation\n\nYou: Hey, I love you.\n" + xfriend + "Thank you, I love you too darling!"
            REPL()
        else:
            print_help()
    else:
        print_help()
