from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, Header, Footer, Static
from textual.widgets import Input, Button
from textual import events
from random import choice
import save
import os

import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

global prompt
prompt = "Imitate my girlfriend. She is cute, smart, a student at Northwestern University, theater major.\n\nYou: Hey, I love you.\nGirlfriend: Thank you, I love you too darling!"

import gf_taka


class Image(Label):
    """Some text."""

class Message(Label):
    """A message"""


class Talk(Static):
    """Some text."""
    def compose(self) -> ComposeResult:
        yield Container(Input(id='input_box'), Button('Talk!', id='talk', variant='success'), id='input_line')
        yield Container(id='messages')

class Wrapper(Static):
    """A textbox."""
    def compose(self) -> ComposeResult:
        yield Container(Image(id='picture'), id='box_pic')
        yield Talk()

class GirlfriendApp(App):
    """A Textual app to talk to your girlfriend."""
    CSS_PATH = "girlfriend.css"
    BINDINGS = [("Ctrl + C", "exit", "Exit")]

    def on_button_pressed(self, event: Button.Pressed) -> None:
            """Event handler called when a button is pressed."""
            if event.button.id == "talk":
                userInput = self.query_one('#input_box').value
                message = gf_taka.talk(userInput)
                self.action_add_message(message)
                images = os.fsencode('images')
                    
                file = os.fsdecode(choice(os.listdir(images)))
                if file.endswith(".miku"): 
                    #print(file)
                    with open('images/'+file) as f:
                        lines = f.read()
                        self.action_update_picture(lines)




    def action_add_message(self, message) -> None:
        """An action to add a new message"""
        new_message = Message(message)
        self.query_one("#messages").mount(new_message)
        new_message.scroll_visible()
    def action_update_picture(self, lines) -> None:
        """An action to update the picture"""
        self.query_one("#picture").update(renderable=lines)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Wrapper()
        yield Footer()





if __name__ == "__main__":
    app = GirlfriendApp()
    app.run()