


import ast
import re

calc_scr_Vname="#coreB"
calc_scr_orgin="__mbd__core__calc"

def calculate(operation):  # the orgin is the function
    return f"scoreboard players operation #coreA __mbd__core__calc {operation}= #coreA __mbd__core__calc\n"


def coppyToRegister(varName, orgin,):  # the orgin is the function
    return f"scoreboard players operation #coreA __mbd__core__calc = #_mdb{varName} _mdb_{orgin}\n"



def dumpIntoScoreboard(varName, orgin):
    return f"scoreboard players operation #_mdb{varName} _mdb_{orgin} = #coreA __mbd__core__calc\n"

def setScore(varname,v):
    global scoreTable
    orgin = "core__calc"
    scoreTable+=f"scoreboard players operation #_mdb{varname} _mdb_{orgin} = {v}\n"
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

def addAToBO(varNameA, varNameB,operation,orgin="core__calc",orginb="core__calc"):  # the orgin is the function

    print(varNameB,varNameA,varNameA.startswith("␀"), varNameB.startswith("␀"))
    global scoreTable
    if (varNameA.startswith("␀")&(not varNameB.startswith("␀"))):
        scoreTable += f"scoreboard players operation #_mdb{varNameB} _mdb_{orginb} {operation}= {varNameA[1:]}\n"
        return varNameB

    elif (varNameB.startswith("␀")&(not varNameA.startswith("␀"))):
        print("fjsqjoipüfghiowedqhioügüholifewhoiühgoüerw")
        scoreTable += f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= {varNameB[1:]}\n"
        return varNameA
    elif (varNameB.startswith("␀")&varNameA.startswith("␀")):
        print("fjsqjoipüfghiowedqhioügüholifewhoiühgoüerw")
        va1=setScore("om1"+varNameA[1:],varNameA[1:])
        va1combined=addAToBO(va1,varNameB,operation,)
        #scoreTable += f"scoreboard players operation #_mdb{va1} _mdb_{orgin} {operation}={varNameB[1:]}\n"
        return va1combined

    scoreTable += f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orginb}\n"
    return varNameA


def addValToA(varNameA, value,operation,orgin="core__calc"):  # the orgin is the function


    global scoreTable
    #print(varNameA,f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orgin}")
    scoreTable+=f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= {value}"
    return  varNameA
def resetCalcReg():
    global scoreTable
    scoreTable+="scoreboard players reset * _mdb_core__calc\n"

scoreTable=""
def functify_aquasion(varname,equation,orgi):
    global scoreTable
    scoreTable=""
    result = parse_expression(equation)
    def calc(r,n=0,literal="a",orginU=""):
        #print(r)
        op,v1,v2=r

        stack=[]
        v1IsOtherVar=False
        v2IsOtherVar = False
        if type(v1) != int:
            if not v1.startswith("#_mdb"):
                v1IsOtherVar=True
        if type(v2) != int:
            if not v2.startswith("#_mdb"):
                v2IsOtherVar=True
        if type(v1)==list:
            v1,fuc=calc(v1,n+1,literal="a")
            stack+=[fuc]


        if type(v2) == list:
            v2,fuc2 = calc(v2,n+1,literal="b")
            stack += [fuc2]
        if type(v1)==int:
            v1 = str(v1)
            print(v1, v1.isdigit())
            if v1.isdigit():
                print("nulified", v1, v1.isdigit())
                #v1=setScore(str(n)+literal,v1)

                v1 = "␀" + str(v1)


        if type(v2) == int:
            v2=str(v2)
            print(v2,v2.isdigit())
            if v2.isdigit():

                v2=setScore(str(n)+literal+"1",v2)
                v2 = "␀" + str(v2)


        #coppyToRegister(f"calc_{v1}{literal}",calc_scr_orgin)
        if n==0:
            ori=orginU
            orib = "core__calc"
        else:
            ori="core__calc"
            orib = "core__calc"
        if v1IsOtherVar:
            vu=v1.split(".",2)
            if len(vu)<2:
                vu+=[orgi]
            n1v = setScore("_calcv1store", 0)
            v2 = addAToBO(n1v, vu[1], "+", orginb=vu[0])

        if v2IsOtherVar:
            vu=v2.split(".",2)
            if len(vu) < 2:
                vu += [orgi]
            n2v=setScore("_calcv2store",0)
            v2=addAToBO(n2v,vu[1],"+",orginb=vu[0])

        match op:
            case "Add":
                #print(v1,v2,ori)
                v=addAToBO(v1,v2,"+",ori,orib)
            case "Mult":
                v=addAToBO(v1,v2,"*",ori,orib)
            case "Sub":
                v=addAToBO(v1,v2,"-",ori,orib)
            case "Div":
                v =addAToBO(v1,v2,"/",ori)

        return v,stack


    addAToBO(varname,calc(result,0,"a",orgi)[0],"",orgi)

    resetCalcReg()

def pr_outVar(varname,func):
    vu = varname.split(".", 2)
    if len(vu) < 2:
        vu += [func]
    return 'tellraw @p [{"text":"'+varname+': ","color":"gold"},{"text":"","color":"red"},{"score":{"name":"'+vu[1]+'","objective":"'+vu[0]+'"}}]'

equation = '0+test'
functify_aquasion("varname",equation,"testfunction")
print("fdw",scoreTable,"--")


