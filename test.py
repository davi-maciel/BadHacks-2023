import os
images = os.fsencode('images')
    
for file in os.listdir(images):
    file = os.fsdecode(file)
    if file.endswith(".miku"): 
        #print(file)
        with open('images/'+file) as f:
            lines = f.read()
            print(lines)
