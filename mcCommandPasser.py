import re
from tkinter.scrolledtext import example

typestr="$str"
typeint="$int"
template={
    "fill":
        "fill $int|~ $int|~ $int|~ $int|~ $int|~ $int|~ $str"
}

allCommands=[
      "advancement",
      "attribute",
      "bossbar",
      "clear",
      "clone",
      "damage",
      "data",
      "datapack",
      "debug",
      "difficulty",
      "effect",
      "enchant",
      "ep",
      "execute",
      "fill",
      "fillbiome",
      "forceload",
      "gamemode",
      "give",
      "help",
      "item",
      "jfr",
      "kill",
      "locate",
      "loot",
      "me",
      "msg",
      "particle",
      "perf",
      "place",
      "playsound",
      "recipe",
      "reload",
      "ride",
      "say",
      "scoreboard",
      "seed",
      "setblock",
      "spawnpoint",
      "stopsound",
      "tag",
      "team",
      "tell",
      "tellraw",
      "title",
      "tp",
      "trigger",
      "w"
]





def isStrconverdiable(test):
    if test.startswith("\"")or (not test.isdigit()):
        return True
    return False

def istype(word,type):
    match type:
        case "$str":
            return  (not word.isdigit())

        case "$int":
            return word.replace(".","").isdigit()
        case _:
            return word==type




def isValid(test):
    wl=test.split(" ")
    #print(wl,wl[0] not in template)
    if wl[0] not in template:

        return []

    templ=template[wl[0]].split(" ")
    errors=[]
    alreadyscaned=""
    try:
        for n,word in enumerate(wl):
            #print(n,word)
            err=[]
            for ty in templ[n].split("|"):
                #print("ty",ty,word)

                if istype(word,ty):
                    err= []
                    break
                err = [(len(alreadyscaned), len(alreadyscaned + word))]

            errors += err
            alreadyscaned += word + " "
    except IndexError:
        errors+=[(len(alreadyscaned),len(test))]
    #print("In templas",errors,test)
    return errors



def parse(lines:[str]):
    errors=[]
    for line in lines:
        allE=[]
        for linings in line.replace(";","\n").split("\n"):
            #print(isValid(linings))

            allE+=isValid(linings)


        errors+= [allE]

    #print("errors",errors)
    return errors


example="fill 12 12 12 12 12 12 minecraft:dirt\n" \
        "fill 3f dj fdf gfds g fd gfd gfd gfd".split("\n")


#print(parse(example))


