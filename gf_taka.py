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

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "The following is a conversation with your girlfriend. Your girlfriend is cute, smart, a student at Northwestern University, theater major"

while True:
    print("You: ")
    userInput = input()
    if userInput == "exit":
        break
    try:
        prompt += "\n\nYou: " + userInput + "\n"
        data = openai.Completion.create(
          model="text-curie-001",
          prompt=userInput,
          temperature=1.0,
          max_tokens=150,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.6,
          stop=[" You:", " Girlfriend:"]
        )
        response = data["choices"][0]["text"];
        prompt += "Girlfriend: " + response
        response = "[magenta]Girlfriend: " + response + "[/magenta]"
        print(response)
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded:", e)
