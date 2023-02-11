#!/usr/bin/env python3
from rich.prompt import Prompt
from rich import box
from rich import print
from rich.panel import Panel

import os
import openai
import json
import typer
import rich

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "The following is a conversation with your girlfriend. Your girlfriend is cute, smart, a student at Northwestern University, theater major"

while True:
    print(f'[hot_pink]You: [/hot_pink]', end='')
    userInput = input()
    
    if userInput == "exit":
        break
    try:
        print(Panel(f'[hot_pink]Girfriend: {userInput}[/hot_pink]', title='CLI Girfriend', box=box.HEAVY, style='orange1'))
    except:
        pass