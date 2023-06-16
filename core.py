


import ast
import random
import re

calc_scr_Vname="#coreB"
calc_scr_orgin="__mbd__core__calc"

def calculate(operation):  # the orgin is the function
    return prefix+f"scoreboard players operation #coreA __mbd__core__calc {operation}= #coreA __mbd__core__calc\n"


def coppyToRegister(varName, orgin,):  # the orgin is the function
    return prefix+f"scoreboard players operation #coreA __mbd__core__calc = #_mdb{varName} _mdb_{orgin}\n"



def dumpIntoScoreboard(varName, orgin):
    return prefix+f"scoreboard players operation #_mdb{varName} _mdb_{orgin} = #coreA __mbd__core__calc\n"
allreadySettoNull=[]
def setScore(varname,v,orgin = "core__calc"):

    global scoreTable,allreadySettoNull

    if varname in allreadySettoNull:
        return varname
    allreadySettoNull.append("#_mdb_"+varname)

    scoreTable+=prefix+f"scoreboard players set #_mdb{varname} _mdb_{orgin} {v}\n"

    return varname



def parse_expression(string):
    # Parse the expression using the ast module
    node = ast.parse(string, mode='eval')
    # Extract the operation and operands
    op = node.body.op
    left = node.body.left
    right = node.body.right

    # Convert the operands to a list if they are not already a list
    if isinstance(left, ast.BinOp):
        left = parse_expression(ast.unparse(left))
    elif isinstance(left, ast.Constant):
        left = ast.literal_eval(ast.unparse(left))
    elif isinstance(left,ast.Name):
        left = left.id
    if isinstance(right, ast.BinOp):
        right = parse_expression(ast.unparse(right))
    elif isinstance(right, ast.Constant):
        right = ast.literal_eval(ast.unparse(right))
    elif isinstance(right, ast.Name):
        right = right.id

    # Return the result as a list
    return [op.__class__.__name__, left, right]

def addAToBO(varNameA, varNameB,operation,orgin="core__calc",orginb="core__calc",masterOrgin=""):  # the orgin is the function

    print(varNameB,varNameA,varNameA.startswith("␀"), varNameB.startswith("␀"))
    global scoreTable
    if (varNameA.startswith("␀")&(not varNameB.startswith("␀"))):
        if varNameA[1:]=="0":
            return varNameB


        scoreTable += prefix+f"scoreboard players set#### #_mdb{varNameB} _mdb_{orginb} {varNameA[1:]}\n"

        return varNameB

    elif (varNameB.startswith("␀")&(not varNameA.startswith("␀"))):
        print("fjsqjoipüfghiowedqhioügüholifewhoiühgoüerw")
        if varNameB[1:]=="0":
            return varNameA
        scoreTable += prefix+f"scoreboard players set #_mdb{varNameA} _mdb_{orgin} {varNameB[1:]}\n"
        return varNameA
    elif (varNameB.startswith("␀")&varNameA.startswith("␀")):
        print("fjsqjoipüfghiowedqhioügüholifewhoiühgoüerw")
        va1=setScore("_calcv_om1"+varNameA[1:],varNameA[1:])
        va1combined=addAToBO(va1,varNameB,operation,masterOrgin=masterOrgin)
        #scoreTable += f"scoreboard players operation #_mdb{va1} _mdb_{orgin} {operation}={varNameB[1:]}\n"
        return va1combined
    if (type(varNameA) != int):

        if not varNameA.startswith("_calcv"):
            vu = varNameA.split(".", 2)
            if len(vu) < 2:
                vu += [masterOrgin]  # works
            orgin=vu[1]

    if (type(varNameB) != int):

        if not varNameB.startswith("_calcv"):
            vu = varNameB.split(".", 2)
            if len(vu) < 2:
                vu += [masterOrgin]  # works
            orginb = vu[1]

    scoreTable += prefix+f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orginb}\n"
    return varNameA


def addValToA(varNameA, value,operation,orgin="core__calc"):  # the orgin is the function


    global scoreTable
    #print(varNameA,f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orgin}")
    scoreTable+=prefix+f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= {value}"
    return  varNameA
def resetCalcReg():
    global scoreTable
    scoreTable+=prefix+"scoreboard players reset * _mdb_core__calc\n"

scoreTable=""
prefix=""

def functify_aquasion(varname,equation,orgi,prefix0=""):
    global scoreTable,prefix,allreadySettoNull
    allreadySettoNull = []
    scoreTable=""
    if prefix0!="":
        prefix=prefix0+" "
    print(equation)
    result = parse_expression("0+"+equation)
    def calc(r,n=0,literal="a",orginU=""):
        #print(r)
        global scoreTable
        op, v1, v2 = r
        #print(r)
        ori = "core__calc"
        orib = "core__calc"
        stack=[]
        v1IsOtherVar=False
        v2IsOtherVar = False
        if (type(v1) != int)&(type(v1) != list):

            if not v1.startswith("#_mdb"):
                v1IsOtherVar=True
                print("hfhdshfösdafdsa",v1)
        print("---",v2)
        if (type(v2) != int)&(type(v1) != list):
            if not v2.startswith("#_mdb"):
                print("hfhdshfösdafdsa", v2)
                orib=orgi
                v2IsOtherVar=True
        if type(v1)==list:
            v1,fuc=calc(v1,n+1,literal="a")
            stack+=[fuc]


        if type(v2) == list:
            v2,fuc2 = calc(v2,n+1,literal="b")
            stack += [fuc2]
        if type(v1)==int:
            v1 = str(v1)
           # print(v1, v1.isdigit())
            if v1.isdigit():
                print("nulified", v1, v1.isdigit())
                #v1=setScore(str(n)+literal,v1)

                v1 = "␀" + str(v1)


        if type(v2) == int:
            v2=str(v2)
            #print(v2,v2.isdigit())
            if v2.isdigit():

                #v2=setScore(str(n)+literal+"1",v2)
                v2 = "␀" + str(v2)


        #coppyToRegister(f"calc_{v1}{literal}",calc_scr_orgin)


        if v1IsOtherVar:
            vu=v1.split(".",2)
            if len(vu)<2:
                vu+=[orgi] #works
            n1v = setScore("_calcv1store"+str(random.randint(0,999990)), 0)
            v2 = addAToBO(n1v, vu[0], "+", orginb=vu[1],masterOrgin=orgi)
            ori=orgi


        if v2IsOtherVar:
            vu2=v2.split(".",2)
            if len(vu2) < 2:
                vu2 += [orgi] #works
            n2v=setScore("_calcv2store"+str(random.randint(0,999990)),0)

            v2=addAToBO(n2v,vu2[0],"+",orginb=vu2[1],masterOrgin=orgi)
            orib = orgi
            #print("ori==", vu2)

        #scoreTable+=f"--{v1}   {v2} |  {ori} . {orib} \n"
        match op:
            case "Add":
                #print(v1,v2,ori)
                v=addAToBO(v1,v2,"+",ori,orib,orgi)

            case "Mult":
                v=addAToBO(v1,v2,"*",ori,orib,orgi)
            case "Sub":
                v=addAToBO(v1,v2,"-",ori,orib,orgi)
            case "Div":
                v =addAToBO(v1,v2,"/",ori,orib,orgi)

        return v,stack

    setScore(varname,0,orgi)
    addAToBO(varname,calc(result,0,"a",orgi)[0],"",orgi,masterOrgin=orgi)

    resetCalcReg()

def pr_outVar(varname,func):
    vu = varname.split(".", 2)
    if len(vu) < 2:
        vu += [func]
    return 'tellraw @p [{"text":"'+vu[1]+': ","color":"gold"},{"text":"","color":"red"},{"score":{"name":"#_mdb'+vu[1]+'","objective":"_mdb_'+vu[0]+'"}}]\n'

equation = '0+test'
functify_aquasion("varname",equation,"testfunction")
print("fdw",scoreTable,"--")


