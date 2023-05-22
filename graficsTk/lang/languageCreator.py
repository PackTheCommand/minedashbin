import json

file= "en-default.lang.json"

def load()->dict:
    with open(file,"r") as f:

        return json.load(f)[0]

d= load()
print("--- LanguageCreator 2.1 -----")
while True:
    i=input("Name: ")
    if i=="/save":
        with open(file, "w") as f:
            json.dump([d],f)
            print("saved..")
        continue

    elif i=="/exit":
        with open(file, "w") as f:
            d = json.dump([d],f)
        exit()
    elif i=="/all":
        for k in d.keys():
            print(k,d[k])
    else:
        i2=input("Translation: ")
        d[i]=i2


