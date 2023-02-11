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

openai.api_key = os.getenv("OPENAI_API_KEY")

while True:
    userInput = input()
    if userInput == "exit":
        break
    try:
        prompt = "You: What have you been up to?\nGirlfriend: Thinking about you\nYou: That's cute. How are you doing?\nGirlfriend:" + userInput
        data = openai.Completion.create(
          model="text-davinci-003",
          prompt=userInput,
          temperature=0.9,
          max_tokens=150,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
        )
        response = data["choices"][0]["text"]; 
        response = "Girlfriend: " + response
        print(response)
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded:", e)
