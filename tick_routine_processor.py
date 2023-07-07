import json
templade=None

def __readTemplade():
    global templade
    if templade==None:
        with open("templates/logic/load.templ") as f:
            templade=json.load(f)

    return templade

def processFuncString(line,calltime=0,funccheckFunction=None):

    a=line.replace(" ","").split("=>")
    

    t=__readTemplade()
    ticka=[]
    maxcounter=len(a)

    for i,func in enumerate(a):
        func_name=funccheckFunction(func)
        s=t["runtime-prefix"]
        ticka+=[s.replace("%function%",func_name).replace("%order%",f"{i}").replace("%n%",f"{calltime}")]


    tickb=[]
    preset=[]+t["scoreboards"]+t["setup"]
    for e in t["tick"]:

        tickb+=[e.replace("%n%",f"{calltime}").replace("%max%",f"{maxcounter}")]

    for i,u in enumerate(preset):
        preset[i]=u.replace("%n%",f"{calltime}").replace("%max%",f"{maxcounter}")

    return {"preset":preset,"tick-section":ticka+tickb}


#print(processFuncString("@on-tick lock_at_players => start",1))