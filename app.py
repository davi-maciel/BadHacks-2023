from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, Header, Footer, Static
from textual.widgets import Input, Button
from textual import events
from random import choice
import save
import os
import argparse
from types import SimpleNamespace

import openai
import re

parser = argparse.ArgumentParser(
                    prog = 'GirlfriendApp',
                    description = 'CLI Girlfriend',
                    epilog = 'Badhacks')

parser.add_argument('-n', '--name', action='store', default='Hatsune Miku', help='Replaces the default girlfriend personality')
parser.add_argument('-k', '--key', action='store', default='', help='Provides the OpenAI key')


args = parser.parse_args()

if not args.key:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    openai.api_key = args.key

global prompt
prompt = f'Imitate my girlfriend. She is {args.name}.\n\nYou: Hey, I love you.\nGirlfriend: Thank you, I love you too darling!'

import gf_taka


image_choice = {
    'Crying': ['crying.miku'],
    'Blushed': ['blush0.miku', 'blush1.miku'],
    'Wink': ['wink0.miku', 'wink1.miku'],
    'Agree': ['agree.miku'],
    'Laughing': ['laughing0.miku', 'laughing1.miku'],
    'Angry': ['angry.miku'],
    'Neutral': ['neutral.miku'],
    'Sad': ['sad.miku'],
    'Confident': ['confident.miku'],
    'Pout': ['pout.miku'],
    'Frown': ['frown.miku'],
    'Puzzled': ['puzzled.miku'],
    'Surprised': ['surprised.miku'],
    'Flirtatious': ['flirtatious.miku']
}


history = []


class Image(Label):
    """Some text."""

class Message(Label):
    """A message"""

class Input2(Input):
    def _on_enter(self, event: events.Enter) -> None:
        return super()._on_enter(event)


class Talk(Static):
    """Some text."""
    def compose(self) -> ComposeResult:
        yield Container(Input2(id='input_box'), Button('Talk!', id='talk'), id='input_line')
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
                global prompt
                userInput = self.query_one('#input_box').value
                message, emotion, prompt2 = gf_taka.talk(userInput, prompt)
                prompt = prompt2
                self.action_add_message(message)
                with open('images/'+choice(image_choice.get(emotion, ['agree.miku']))) as f:
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
        #yield Header()
        yield Wrapper()
        #yield Footer()





if __name__ == "__main__":
    app = GirlfriendApp()
    app.run()