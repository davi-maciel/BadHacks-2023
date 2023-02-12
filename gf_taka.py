#!/usr/bin/env python3

# import sys
# def standard_response():
#    print("How are you doing today, honey?")

# def hello():
#    print("Hi! How are you doing today?")

#if __name__ == "__main__":
#    if len(sys.argv) == 1:
#        standard_response()
#    elif sys.argv[1] == "hello":
#        hello()

import os
import openai
import json
import typer
import rich
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "Imitate my girlfriend. She is cute, smart, a student at Northwestern University, theater major.\n\nYou: Hey, I love you.\nGirlfriend: Thank you, I love you too darling!"

def get_response(fullPrompt):
    data = openai.Completion.create(
        model="text-curie-001",
        prompt=fullPrompt,
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Girlfriend:"]
    )
    response = data["choices"][0]["text"];
    return response

def talk(userInput):
    try:
        prompt = prompt + "\nYou: " + userInput + "\nGirlfriend: "

        response = get_response(prompt)

        # Remove weird blank spaces from beginning and end of response
        response = re.sub("^\s*", "", response)
        response = re.sub("\s*$", "", response)


        prompt = prompt + response;
        return "Girlfriend: " + response

    except openai.error.RateLimitError as e:
        return "Rate limit exceeded: " + e


while True:
    print("You: ", end='')
    userInput = input()
    if userInput == "exit":
        print(prompt)
        break
    print(talk(userInput))

