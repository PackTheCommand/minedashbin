import json


typestr="$str"
typeint="$int"
typeany="$*any"
template={}
allCommands=[]
def getCommands():
    global allCommands,template

    with open("comver/--newest.minfo") as f:
        l = json.load(f)
    template=l[0]
    allCommands=list(l[0].keys())



getCommands()
#print(allCommands)



def isStrconverdiable(test):
    if test.startswith("\"")or (not test.isdigit()):
        return True
    return False

def istype(word,type):
    #print("ww",word,type)
    match type:
        case "$str":

            return  (not word.isdigit())

        case "$int":

            return word.replace(".","").isdigit()

        case _:
            return word==type




def isValid(test):
    wl=test.split(" ")
    #print("1",wl,wl[0] not in template,wl[0], template["msg"])
    if wl[0] not in template:

        return []

    templ=template[wl[0]].split(" ")
    errors=[]
    alreadyscaned=""
    done = False
    try:
        for n,word in enumerate(wl):
            #print(n,word)
            if done:
                break
            err=[]
            for ty in templ[n].split("|"):
                #print("ty",ty,word)
                if ty==typeany:
                    done=True
                    break

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


"""example="msg 543\n" \
        "".split("\n")
"""

"""print(parse(example))
"""

