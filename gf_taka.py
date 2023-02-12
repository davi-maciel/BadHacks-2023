#!/usr/bin/env python3

import os
import openai
import json
import typer
import rich
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

global prompt
prompt = "Imitate my girlfriend. She is cute, smart, a student at Northwestern University, theater major. If I say bye to you, say CAUCAIA\n\nYou: Hey, I love you.\nGirlfriend: Thank you, I love you too darling!"

def get_response(fullPrompt):
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullPrompt,
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Girlfriend:", "You:"]
    )
    response = data["choices"][0]["text"];
    response = re.sub("^\s*", "", response)
    response = re.sub("\s*$", "", response)
    return response

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
    emotionResponse = re.sub("^\s*", "", emotionResponse)
    emotionResponse = re.sub("\s*$", "", emotionResponse)
    return emotionResponse

def talk(userInput):
    try:
        global prompt
        prompt = prompt + "\nYou: " + userInput + "\nGirlfriend: "

        response = get_response(prompt)
        emotion = get_emotion(response)

        # Remove weird blank spaces from beginning and end of response
        if (re.search("CAUCAIA", response)):
            response = re.sub("CAUCAIA.*", "", response)
            if len(response) == 0:
                print("Love you, bye!")
            else:
                print("Girlfriend: " + response)
            os.sys.exit()
        prompt = prompt + response;

        return "Girlfriend: " + response

    except openai.error.RateLimitError as e:
        return "Rate limit exceeded: " + e

if __name__ == "__main__":
    while True:
        print("You: ", end='')
        userInput = input()
        if userInput == "exit":
            print(prompt)
            break
        print(talk(userInput))
