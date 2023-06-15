


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
        left = "#_mdb"+left.id
    if isinstance(right, ast.BinOp):
        right = parse_expression(ast.unparse(right))
    elif isinstance(right, ast.Constant):
        right = ast.literal_eval(ast.unparse(right))
    elif isinstance(right, ast.Name):
        right = "#_mdb"+right.id

    # Return the result as a list
    return [op.__class__.__name__, left, right]

def addAToBO(varNameA, varNameB,operation,orgin="core__calc"):  # the orgin is the function


    global scoreTable
    #print(varNameA,f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orgin}")
    scoreTable+=f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orgin}\n"
    return  varNameA

def addValToA(varNameA, value,operation,orgin="core__calc"):  # the orgin is the function


    global scoreTable
    #print(varNameA,f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orgin}")
    scoreTable+=f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= {value}"
    return  varNameA
def resetCalcReg():
    global scoreTable
    scoreTable+="scoreboard players reset * _mdb_core__calc\n"

scoreTable=""
def functify_aquasion(equation,orgi):
    global scoreTable
    scoreTable=""
    result = parse_expression(equation)
    def calc(r,n=0,literal="a",orginU=""):
        print(r)
        op,v1,v2=r

        stack=[]


        if type(v1)==list:
            v1,fuc=calc(v1,n+1,literal="a")
            stack+=[fuc]


        if type(v2) == list:
            v2,fuc2 = calc(v2,n+1,literal="b")
            stack += [fuc2]
        if type(v1)==int:
            v1 = str(v1)
            if v1.isdigit():


                v1=setScore(str(n)+literal,v1)


        if type(v2) == int:
            v2=str(v2)
            if v2.isdigit():

                v2=setScore(str(n)+literal+"1",v2)

        #coppyToRegister(f"calc_{v1}{literal}",calc_scr_orgin)
        if n==0:
            ori=orginU
        else:
            ori="core__calc"

        match op:
            case "Add":
                v=addAToBO(v1,v2,"+",ori)
            case "Mult":
                v=addAToBO(v1,v2,"*",ori)
            case "Sub":
                v=addAToBO(v1,v2,"-",ori)
            case "Div":
                v =addAToBO(v1,v2,"/",ori)

        return v,stack

    calc(result,0,"a",orgi)
    resetCalcReg()


equation = '4*48+3*test+(18*5)'
functify_aquasion(equation,"test")
print("fdw",scoreTable,"--")


