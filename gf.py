import sys
def standard_response():
    print("How are you doing today, honey?")

def hello():
    print("Hi! How are you doing today?")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        standard_response()
    elif sys.argv[1] == "hello":
        hello()
    