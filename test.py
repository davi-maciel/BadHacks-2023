import os
images = os.fsencode('images')
    

api_key = os.getenv("OPEAI_API_KEY")

print(api_key)

for file in os.listdir(images):
    file = os.fsdecode(file)
    if file.endswith(".miku"): 
        print(file)
        #with open('images/'+file) as f:
        #    lines = f.read()
