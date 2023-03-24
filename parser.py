import json
import os
import random
import re
import shutil
import time

import setings

import templade, exeptions_

minecraft_commands=["execute","fill","say","datapack","debug","help","jfr","setblock",
                    "locate","perf","reload","scoreboard","seed","me","msg","tell",
                    "tellraw","w","advancement","attribute","bossbar","clear","damage","data","effect","enchant","ep",
                    "gamemode","give","item","kill","loot","particle","playsound","recipe","ride","spawnpoint",
                    "stopsound","tag","team","tp","title","trigger","clone",
                    "difficulty","place","fillbiome","forceload","data"]

from sys import argv
Seti= setings.Settings("settings.json")
def create_project():
    name=input("Project Name: ")
    sourcefile=input("Main file: ")

    print("Project Name: "+name+" ,Source File: "+sourcefile)
    yn=input("Create project? (y/n)")
    if yn=="y":

        r=random.randint(1,9999999)
        while str(r) in Seti.get("pr_ids"):
            r = random.randint(1, 9999999)

        print("creating files")
        Seti.get("All-Projects")[r]={"name": name, "source": sourcefile}

        yn = input("Set as Current Project ? (y/n)")
        if yn == "y":
            Seti.set("Current-Project",str(r))
        Seti.save()


if len(argv)>=2:
    if "--new" in argv:
        create_project()
    for s in argv:
        if s.startswith("--project"):
            u,p=s.split("=",1)
            prlist=Seti.get("All-Projects")
            for i in prlist.keys():
                if p in prlist[i]["name"]:
                    Seti.set("Current-Project",i)
    """if not ("--c" in argv or "--compile" in argv):
        print("no args provided, use '--c' to compile on next run")
        exit(0)"""

if Seti.get("All-Projects")=={}:
    print("Error:","No project found, specify a project with '--new'")
    exit()

projectName = Seti.get("All-Projects")[Seti.get("Current-Project")]["name"]
FILE=Seti.get("All-Projects")[Seti.get("Current-Project")]["source"]



paser_keywords_corespontents = {}

num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", " "]
hasch = ["#", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f"]
def getStringSeperated(string,splitonspace=True):
    retStr=[""]

    enter=False
    disabled=False
    for char in string:
        if splitonspace&(char==" ")&(not enter):
            retStr[-1] += char
            retStr += [""]
            continue

        if ((char == "\"")|(char == "'"))&(not disabled):

            enter=not enter
            if enter:
                retStr += [""]
            else:
                retStr[-1] += char
                retStr += [""]
                continue
        if disabled:
            disabled=False
        if (char == "\"")&enter:
            disabled=True
        if enter:
            add=True

        retStr[-1]+=char
    return retStr

#print(getStringSeperated("test# 'test'"))
#exit()


def list_remove_empty(list):
    while "" in list:
        list.remove("")
    return list



parserCCCBeginWords=[]
def trygetAddType(str):
    inStr = False
    defChars = ["+", "-", "=", "*", "/"]
    result = []
    snow = ""
    charBuffer = ""
    signalWrite = False
    ch = ""
    for char in str:

        disableSTdef = False
        if (not signalWrite) & (snow != ""):
            result += [("eq", snow)]
            snow = ""
        signalWrite = False
        if char == "\\":
            disableSTdef = True
        elif char == "\"":
            if not disableSTdef:
                inStr = not inStr
        elif char in defChars:

            if not disableSTdef:
                if snow == "":
                    result += [("v", charBuffer)]
                    charBuffer = ""
                signalWrite = True
                snow += char
        if not signalWrite:
            if not disableSTdef:
                if char == " ":
                    continue
            charBuffer += char
        ch += char
    if snow != "":
        result += [("eq", snow)]
    if charBuffer != "":
        result += [("v", charBuffer)]

    return result


def getType(value: str):
    value = value.replace(" ", "")
    if value.startswith("#"):
        if checkIfCharValid(value[1:], hasch):
            return "#"
    elif (value.startswith("\"") & value.endswith("\"")) or (value.startswith("'") & value.endswith("'")):

        return "str"
    else:
        if checkIfCharValid(value, num):
            return "num"
    return "obj"


def checkIfCharValid(str, list):
    for char in str:


        if char not in list:
            return False
    return True



def creComp(optype,payload,requires=None):
    return {"op": optype ,"payload":payload,"requires":requires}


class NewParser:
    def __init__(self, name="this."):
        self.name = name
        self.tree = []
        self.file = FILE
        self.pointer = [0]
        self.section = ""
        self.form = []
        self.shorts = {}
        self.files = {}
        self.functionVariableScoreboards = []
        self.ScoreboaRD_delete=""
        self.funcs = {"main": []}
        self.func_takes = {}
        self.include = []
        self.str_func_def_block = ""
        self.special_ops_files = []
        self.text=""
        self.blocks = {"_include": [], "_jumper": "", "_funcvar": [], "_allVars": {}}
        # self.section= {}

    def load(self,file=""):
        if file=="":
            with open(self.file, "r") as f:
                self.text += f.read().replace("  ","")
        else:
            with open(file, "r") as f:
                self.text += f.read().replace("  ","")

    def parse(self):

        insideString=False
        escaped=False
        linehasSimicolon=False
        lineisEmpty=True
        lineNum=1
        inComment=False
        stringOpendInLine=0

        for charNr,char in enumerate(self.text):

            tree = self.getPoint()
            if char not in [" ","\n"]:
                lastchar=char

            if (char!=" ")&(char!="\n")&(char not in ["{","}","[","]",";"]):
                lineisEmpty=False


            if char==";":
                linehasSimicolon=True

            #if line BreakProcedure

            if ((self.text[charNr - 1]== "/")&(char=="/")&(not insideString)&(not inComment)):
                print("Entered comment",bytes(self.text[charNr-2],"UTF-8"))
                if (not(self.text[charNr-2] in "{}[]\n")):

                    if linehasSimicolon|lineisEmpty:
                        lineisEmpty=True
                        linehasSimicolon=False

                    else:
                        exeptions_.MissingSimicolon(lineNum-1)

                if insideString:
                    exeptions_.StringNeverClosedErr(stringOpendInLine)
                inComment=True
                self.section=self.section[:-2]

            if char=="\n":

                lineNum += 1
                if inComment:
                    print("LEntered comment")

                    inComment=False
                    continue

                if (not(self.text[charNr-1] in "{}[]\n")):

                    if linehasSimicolon|lineisEmpty:
                        lineisEmpty=True
                        linehasSimicolon=False

                    else:
                        print("com",char,)
                        exeptions_.MissingSimicolon(lineNum-1)

                if insideString:
                    exeptions_.StringNeverClosedErr(stringOpendInLine)

                continue
            if inComment:
                print("skipp ",char)
                continue
            if ((char == "\"") | (char == "'")) & (not escaped):
                stringOpendInLine=lineNum

                insideString = not insideString

            if escaped:
                escaped = False
            if (char == "\\") & insideString:
                stringOpendInLine=lineNum
                escaped = True

            if (((char == "{") | (char == "}") | (char == "(") | (char == ")") | (char == "[") | (char == "]") | (
                    char == ";"))&(not insideString)):

                if self.section != "":
                    # #print(self.section)
                    self.form += [self.section]
                    self.section = ""
                    # #print("char",char)
                if char != ";":
                    self.form += [char]

            else:
                self.section += str(char)

        self.form += self.section




    def toStruncktree(self):
        pass

    def wr(self):
        with open(self.file + ".form", "w") as f:
            f.write(str(self.form))

    def getPoint(self):
        l = self.tree
        try:
            for i in self.pointer:
                l = l[i]
            return l
        except Exception:
            return None

    def toCode(self):
        funcName = "none"
        enter = False

        nextagon = "n"
        NoLeave = []
        i = 0
        while i < len(self.form):
            e = self.form[i]
            if e.startswith("func"):
                s = e.split(" ")
                funcName = self.name + s[1]
                ##print("nfn", funcName)
                self.funcs[funcName] = []
                self.func_takes[funcName] = []
                nextagon = "ARGS-0"
                enter = True
                ##print("func")
                i += 1
                pass

            elif e.startswith("{"):

                if nextagon == "FUNC-BLOCK":
                    pi = i
                    if enter:
                        sc = ""
                        between = []

                        while sc != "}":

                            between += [self.form[pi]]
                            pi += 1
                            try:
                                sc = self.form[pi][0]  # sc is a char , pi is a string
                            except IndexError:
                                exeptions_.BrackedNeverClosed(i)

                        i = pi + 1
                        between.pop(0)
                        self.funcs[funcName] = between
                        funcName = "none"
                        enter = False
                        nextagon = "n"

                    else:
                        NoLeave += "0"

                    pass
            elif e.startswith("("):

                if enter:
                    if nextagon == "ARGS-0":
                        pi = i + 1
                        sc = self.form[pi]
                        between = ""
                        takes_args_count = 0
                        while sc != ")":
                            takes_args_count += 1
                            # sc is a char , pi is a string
                            between += self.form[pi]
                            pi += 1
                            sc = self.form[pi][0]
                        i = pi + 1
                        count = between.count(",") + 1
                        if between == "":
                            count = 0
                        self.func_takes[funcName] = (count, between)
                        nextagon = "FUNC-BLOCK"
                else:
                    self.funcs["main"] += [e]
                    i += 1


            else:

                i += 1

                self.funcs["main"] += [e]

    def get(self):
        pass
        # print(self.form)
        # print(self.func_takes)
        # print(self.funcs)

    def initializeCompileReferenceKeywords(self):

        for a in [] + (self.funcs["main"]):
            # #print("cw",self.funcs["main"])
            # #print(">>>",a)
            if a.startswith("cc"):
                self.funcs["main"].remove(a)
                fn = a.split(" ")[-1]

                self.special_ops_files += [fn]

    def declerationfileSerch(self):
        for file in self.special_ops_files:
            try:
                with open("cc/" + file + ".ccc") as f:

                    jl = json.load(f)
                    for component in jl:
                        kww = component["kww"]
                        synt = component["syntax"]
                        handler = component["interface"]
                        if handler == "Nothing":

                            paser_keywords_corespontents[kww] =  synt.replace("<<prName>>",projectName)
                        else:
                            if kww not in paser_keywords_corespontents:
                                paser_keywords_corespontents[kww] = "@C-had " + handler + " " + str(
                                    synt.count("%s")) + " " + synt
                            else:
                                exeptions_.ccFileError(" <was trying to overwrite existing interface '" + kww + "'>",
                                                       file)

            except KeyError:
                exeptions_.ccFileError(" <missing link components>", file)
            except FileNotFoundError as e:

                exeptions_.ccFileError(" <File-Does-Not-Exist>", file)
            except json.decoder.JSONDecodeError:
                exeptions_.ccFileError(" <JsonFileInvalid>", file)
            except Exception:
                exeptions_.ccFileError(" <Exception>", file)

    def createBlockInclude(self):
        l = []
        na = []
        for a in [] + (self.funcs["main"]):
            # #print("cw",self.funcs["main"])
            # #print(">>>",a)

            self.blocks["nativeImport"]=[]
            if a.startswith("include"):
                self.funcs["main"].remove(a)
                l+=[a.replace("include","").replace(" ","")]
                self.blocks["_include"] += [a.split(" ")[-1]]

            if a.startswith("native"):
                na+=[a.split(" ")[-1]]
                self.funcs["main"].remove(a)

        return l,na

    def functionexecutionBlock(self):

        for key in self.funcs.keys():
            if key == "main":
                funcKey="main"
            else:
                funcKey=key
            s = []

            self.files[key]=[]

            for line in self.funcs[funcKey]:
                if line["payload"].replace(" ", "") != "":
                    s += [line]
            self.files[key] += s

    def creteFuncVaribleBlock(self):

        for key in self.func_takes:
            if key == "main":
                continue
            n, parms = self.func_takes[key]

            for n, p in enumerate(parms.split(",")):
                name = key + "." + p
                self.blocks["_funcvar"] += [name]

    def createFuncBlock(self):

        b = "section _deffunc\n"
        for key in self.funcs.keys():

            if key == "main":
                continue

            argsC, argsN = self.func_takes[key]
            key = key.replace("this.", "")
            b += templade.getFuncTemplate(key, argsC, argsN.split(","))
            fc = "scoreboard objectives add _mdb_" + key + " dummy\n"
            for arg in argsN.split(","):
                # print("args123",arg)
                fc += "scoreboard players set #_mdb_" + arg + " _mdb_" + key + " 0\n"
            self.ScoreboaRD_delete+="scoreboard objectives remove _mdb_" + key+"\n"
            self.functionVariableScoreboards += [fc]
        # #print("bi",b)
        self.str_func_def_block = b

    def creteMain(self):
        pass

    def createFile(self,requires,includes):
        global projectName
        fx = ".mcfunction"
        pathfunc="out/" + projectName + "/data/" + projectName + "/functions"

        if not os.path.exists(pathfunc):
            os.makedirs(pathfunc)
        if not os.path.exists("out/" + projectName + "/pack.mcmeta"):
            shutil.copyfile("templates/pack.png", "out/" + projectName + "/pack.png")
            shutil.copyfile("templates/pack.mcmeta", "out/" + projectName + "/pack.mcmeta")

        with open("out/" + projectName+"/" + "general.info", "w") as f:
            s="Created with ...\n" \
              "Version 1.0.1\n" \
              "\n" \
              "---Native-Module Imports---\n"



            f.write(s)


            for i in requires:
                f.write(i+"\n")
            f.write("---Module Imports---\n")
            for i in includes:
                f.write(i)
        with open(pathfunc+ "/_mbd_scoreboards" + fx, "w") as f:
            for a in self.functionVariableScoreboards:
                f.write(a)

        with open(pathfunc+ "/routine_del_cleanup" + fx, "w") as f:

            f.write(self.ScoreboaRD_delete)
        #print("keys", self.files)
        for a in self.files.keys():

            with open(pathfunc + "/_mbd_" + a.replace("this.", "") + "_" + fx, "w") as f:
                # a is the filename

                if type(self.files[a])==list:
                    #print("skipp")
                    continue
                f.write(self.files[a])


            #print("requires",requires)
        for filep in requires:
            p="templates/baselib/"+filep
            if os.path.exists(filep+".mcfunction"):
                #print("copied",filep)
                shutil.copyfile(filep+".mcfunction",pathfunc+"/"+filep.split("/")[-1]+".mcfunction")
            elif os.path.exists(p+".mcfunction"):
                #print("copied",filep)
                shutil.copyfile(p+".mcfunction",pathfunc+"/"+filep.split("/")[-1]+".mcfunction")
            else:
                exeptions_.nativeModulerNotFound(filep)

    def identify_ops(self):
        nextOPConditon = None
        def newComp(optype,payload):
            nonlocal nextOPConditon
            r=creComp(optype,payload,requires=nextOPConditon)
            nextOPConditon = None
            return r



        for ins in range(0, len(self.funcs.keys())):
            key = list(self.funcs.keys())[ins]
            lineList = self.funcs[key]
            newList = []
            nextOPConditon=None
            # newList += ["@fc "]
            li = -1
            while li in range(-1, len(lineList) - 1):
                li += 1

                string = self.funcs[key][li]
                fs = re.sub("\s\s+", " ", string)
                # print("<<<",fs)
                Slist = re.split(",|=| ", fs)
                # print("<<< ",Slist)
                # #print(Slist)
                #print(Slist,minecraft_commands.count(Slist[0]),minecraft_commands)
                if "this." + Slist[0] in self.funcs.keys():
                    ##print(f"{Slist[0]} is a function")
                    args = ""
                    pi = 1
                    sl = lineList[li + pi]

                    while sl != ")":
                        sl = lineList[li + pi]
                        args += sl + " "
                        pi += 1
                    if (pi > 9999):
                        exeptions_.parameterLimitReched(li)
                    li += pi - 1
                    newList+=[newComp("@fc","this." + Slist[0] + " " + str(pi) + " " + args[1:-2])]
                    #newList += ["@fc this." + Slist[0] + " " + str(pi) + " " + args[1:-2]]
                    ##print(Slist[0], args[1:-2])
                elif key + "." + Slist[0] in self.blocks["_funcvar"]:

                    newList += [newComp("@v-f" , lineList[li])]
                    pass

                elif (Slist[0] in minecraft_commands):

                    newList +=[newComp("@nai",lineList[li])]
                elif Slist[0].startswith("#if"):
                    nextOPConditon=lineList[li]
                    continue

                elif Slist[0].startswith("shr"):
                    shl=string.split(" ")
                    if len(shl)!=3:
                        exeptions_.schortGivenToMuchArgs(string)
                    else:
                        kww,name,short=shl
                        self.shorts[name]=short
                elif Slist[0].startswith("inject"):

                    newList += [newComp("@inj" , lineList[li][7:])]
                elif ((len(fs) > len(Slist[0]))):

                    if (fs[len(Slist[0])] == "="):
                        # print(".,",Slist[0])

                        name = key + "." + Slist[0]
                        ##print("TempVar")

                        forml = trygetAddType(lineList[li])

                        # print("forml",forml,lineList[li])
                        # print(forml[2])
                        typeofVAR = getType(forml[2][1])

                        setVar = ""

                        for e in forml:
                            if e[0] == "v":
                                setVar += "." + e[1] + " "
                            else:
                                setVar += "$" + e[1] + " "

                        newList += [newComp("@v-l" , setVar + typeofVAR)]

                        if name not in self.blocks["_allVars"]:
                            self.blocks["_allVars"][name] = Slist[1]


                    elif (Slist[0].split(" ")[0] in paser_keywords_corespontents.keys()): #todo : implement new cc system #migration
                        # print("--")
                        # print()
                        # print(Slist)
                        # print("sl",Slist[0])#
                        # print("__")
                        try:
                            line = []
                            line += Slist
                            line.pop(0)
                            placein=list_remove_empty(getStringSeperated((fs.split(" ",1)[1])))
                            countkww=len(placein)
                            #print(countkww,placein,paser_keywords_corespontents[Slist[0]],fs)
                            counttakes=paser_keywords_corespontents[Slist[0]].count("%s")

                            newList += [newComp("@cc-inj",paser_keywords_corespontents[Slist[0]] % tuple(i for i in placein))]

                        except Exception as e:

                            exeptions_.kww_missing_arguments(li, Slist[0], countkww, counttakes)

                        pass
                    else:
                        # print(Slist)
                        if (Slist[0].startswith("@")):
                            continue
                        elif Slist[0].startswith("I..I"):
                            continue
                        #print("operator","'"+str(Slist)+"'")
                        if Slist[0]=="":
                            exeptions_.indexiationError(string, "?")
                        exeptions_.unknownOperator(Slist[0], "?")
                else:
                    exeptions_.unableToUnderstandInstrucktion(string,"?")
                    pass
                    """
                    try:
                        pass
                        # print("1234","'"+str(len(Slist[0]))+Slist[1]+"'",len(Slist[0]),Slist)
                    except:
                        pass
                    ##print("line", key + "." + Slist[0], self.blocks["_funcvar"])"""
                del Slist, fs
            self.funcs[key] = newList
    def removeStringIdentifier(self,str1:str,prefixignore="i"):
        if str1.startswith("\"")|str1.startswith("'"):
            str1=str1[1:]
            if str1.endswith("\"") | str1.endswith("'"):
                str1 = str1[:-1]
        elif str1.startswith(prefixignore):
            return str1[1:]
            pass

        return str1

    def replaceShort(self,line):
        str1list=getStringSeperated(line,False)
        ret=""
        for item in str1list:
            if not(item.startswith("\"")|item.startswith("'")):
                for short in self.shorts.keys():

                    if item.count("<"+short+">")>0:

                        item=item.replace("<"+short+">",self.removeStringIdentifier(self.shorts[short]))
            ret+=item
        return ret

    def Variabels_mine_format(self):

        """o=open("fjkdshjijhfdsjaö.txt", "w")

        for f in self.files.keys():
            o.write("----"+f+"-----\n")
            o.write(self.files[f])
        o.close()"""
        print("allfuncs",list(self.files.keys()))
        for filename in list(self.files.keys()):


            old_lines = self.files[filename]
            print(old_lines,filename)
            filename = filename.replace("this.", "")
            formatedLines = ""
            linePointer = 0
            allLines = old_lines
            while linePointer < len(old_lines):
                #print("spm",allLines[linePointer],type(allLines[linePointer]))
                opX = allLines[linePointer]["op"]
                requires=allLines[linePointer]["requires"]
                #print(opX)

                line = self.replaceShort(allLines[linePointer]["payload"])


                linePointer += 1

                if requires!=None:
                    #todo impemantation of if statments
                    pass

                if opX=="@v-l":
                    print("varfounf",line)

                    ls = line.split(" ")

                    #print("val",ls)
                    sc_name = ls[0].replace("this.", "")
                    operation = ls[1].replace("$", "")
                    add_to_sc = ls[2].replace("this.", "")

                    sc_type = ls[3]
                    print(sc_name,operation,add_to_sc,sc_type,opX)
                    l = ""
                    if operation != "=":

                        if sc_type != "num":
                            # todo
                            l = "scoreboard players operation #_mdb_" + sc_name + " _mdb_" + filename + " " + operation + " " + "#_mdb_" + add_to_sc + " " + filename

                        elif sc_type != "obj":
                            if add_to_sc.count(".") > 0:
                                orgin, varname = add_to_sc.split(".", 1)
                                l = "scoreboard players operation #_mdb_" + sc_name + " _mdb_" + filename + " " + operation + " ""#_mdb_" + varname + " "
                            else:
                                l = "scoreboard players operation #_mdb_" + sc_name + " _mdb_" + filename + " " + operation + " " + "#_mdb_" + add_to_sc + " " + filename

                    else:

                        if sc_type == "num":

                            l = "scoreboard players set #_mdb_" + sc_name + " _mdb_" + filename + " " + add_to_sc.replace(
                                ".", "")
                        elif sc_type == "obj":

                            if (not add_to_sc.replace(" ", "").startswith(".")):
                                orgin, varname = add_to_sc.split(".", 1)

                                l = "scoreboard players operation #_mdb_" + sc_name + " _mdb_" + filename + " = " + "#_mdb_" + varname + " _mdb_" + orgin + " " + add_to_sc
                            else:
                                l = "scoreboard players operation #_mdb_" + sc_name + " _mdb_" + filename + " = " + "#_mdb_" + add_to_sc + " _mdb_" + filename
                        else:

                            l = ""
                    print(l)
                    formatedLines += l + "\n"
                elif opX=="@inj":

                    formatedLines+=self.removeStringIdentifier(line[6:])+"\n"
                elif opX=="@nai":
                    formatedLines+=line+"\n"
                elif opX=="@cc-inj":
                    formatedLines+=line+"\n"

                elif opX=="@fc":
                    #print("funccall",line)
                    ls = line.split(" ", 6)
                    #print("search",ls)

                    #print("ls",ls)
                    funcName = ls[0].replace("this.", "")

                    args = ls[3]

                    argsCount=args.count(",")+1
                    if args.replace(" ","")=="":
                        argsCount=0

                    sc_type = ls[3].replace(" ", "")

                    varNames = self.blocks["_funcvar"]
                    try:
                        takescount, takesargs = self.func_takes["this." + funcName]
                    except:
                        #print(line)
                        exeptions_.functionDoesntExist(funcName)
                        return "END_OF_PROGRAM_BY_EXCEPTION"
                    takesargsSplit=takesargs.split(",")
                    #print(funcName,int(argsCount), takescount)
                    if int(argsCount) != takescount:


                        #print(type(argsCount),type(takescount),line)
                        exeptions_.parameterCountNotMacking(funcName, takescount, argsCount)

                    for n, var in enumerate(args.split(",")):
                        varname = "self.func_takes"
                        vartype = getType(var)

                        ins = creComp("@v-l",f".{funcName}.{takesargsSplit[n]} $= .{var} {vartype}")


                        allLines.insert(linePointer + n, ins)

                    formatedLines += "schedule function " + projectName + ":_mbd_" + funcName + " 1t\n"


                else:

                    if opX=="I..I":
                        # print(line)
                        if opX == "I..I":
                            strlist = getStringSeperated(s, False)
                            fstr = ""
                            n = len(strlist)
                            firstline = True

                            while n >= 0:
                                st = strlist[n]
                                if firstline:
                                    firstline = False

                                fstr += self.removeStringIdentifier(st, "k")
                                n -= 1
                                formatedLines += fstr

                            formatedLines += line
                    else:
                        print("rejected",line,opX)

            if filename!="main":
                self.files["this."+filename] = formatedLines
            else:
                self.files[filename] = formatedLines
        print(self.files)

includes=[]
requires=[]
start_time = time.time()
try:
    print("Starting...")
    print("Querying Module imports...")
    while True:

        p = NewParser()
        p.load()
        for incl in includes:
            if os.path.exists(incl + ".mdblib"):
                p.load(incl + ".mdblib")
            elif os.path.exists("templates/baselib/" + incl + ".mdblib"):
                p.load("templates/baselib/" + incl + ".mdblib")
            else:
                exeptions_.ModuleNotFound(incl)


        p.parse()
        #p.wr()
        p.toCode()
        includesNew, requiresNew=p.createBlockInclude()

        if (includesNew==includes)and(requiresNew==requires):

            break
        includes,requires = includesNew,requiresNew
    print("Compiling-Started...")
    p.createFuncBlock()
    p.initializeCompileReferenceKeywords()
    p.declerationfileSerch()
    p.creteFuncVaribleBlock()
    print("Analyzing-Operations...")
    p.identify_ops()
    print("Generating-Functions...")
    p.functionexecutionBlock()

    """for key in paser_keywords_corespontents.keys():
        parserCCCBeginWords+=paser_keywords_corespontents[key].split(" ")[0]"""
    print("Converting to mcfunction format...")
    p.Variabels_mine_format()
    print("Safing to file...")
    p.createFile(requires,includes)

    end_time = time.time()
    print("Finished after",round(end_time-start_time,6)*1000,"ms")
    e = time.time()
    time.sleep(0.001)

except OSError as e:
    exeptions_.CompilationError(e)

