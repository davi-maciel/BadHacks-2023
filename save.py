import json

def save(content: dict, file_name='data.json'):
    with open(file_name, 'w') as file:
        file.write(json.dumps(content))
def load(file_name='data.json'):
    with open(file_name, 'r') as file:
        return json.load(file)