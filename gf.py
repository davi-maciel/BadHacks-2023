import sys
def standard_response():
    print("How are you doing today, honey?")

def hello():
    print("Hi! How are you doing today?")

def tired():
    print("What made you tired? :(")

while True:
    usr_input = input()
    if usr_input == "hello":
        hello()
    elif usr_input.find("tired") != -1:
        tired()
    