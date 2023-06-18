import ast
import random

idToOrginRegister = {}

allreadySettoNull = []


def setScore(varname, v, orgin="core__calc"):
    global scoreTable, allreadySettoNull

    if varname in allreadySettoNull:
        return varname
    allreadySettoNull.append("#_mdb_" + varname)
    idToOrginRegister[varname] = orgin

    scoreTable += prefix + f"scoreboard players set #_mdb{varname} _mdb_{orgin} {v}\n"

    return varname


def parsePredefined(master, art):
    """here later predefined parameters can be added"""
    return master, art


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
    elif isinstance(left, ast.Name):
        left = left.id
    elif isinstance(left, ast.Attribute):
        o, a = parsePredefined(ast.unparse(left.value).strip(), left.attr)
        left = f"{o}.{a}"
    else:
        print("Ast-tree-Error [Please Report Case]  [left]", left)
        exit()

    if isinstance(right, ast.BinOp):
        right = parse_expression(ast.unparse(right))
    elif isinstance(right, ast.Constant):
        right = ast.literal_eval(ast.unparse(right))
    elif isinstance(right, ast.Name):
        right = right.id
    elif isinstance(right, ast.Attribute):
        right = f"{ast.unparse(right.value).strip()}.{right.attr}"
    else:
        print("Ast-tree-Error [Please Report Case]  [right]", right)
        exit()
    # Return the result as a list
    return [op.__class__.__name__, left, right]


def addAToBO(varNameA, varNameB, operation, orgin="core__calc", orginb="core__calc",
             masterOrgin=""):  # the orgin is the function
    if varNameA in idToOrginRegister.keys():
        orgin = idToOrginRegister[varNameA]
    if varNameB in idToOrginRegister.keys():
        orginb = idToOrginRegister[varNameB]

    global scoreTable
    if (varNameA.startswith("␀") & (not varNameB.startswith("␀"))):
        if varNameA[1:] == "0":
            return varNameB

        scoreTable += prefix + f"scoreboard players add #_mdb{varNameB} _mdb_{orgin} {varNameA[1:]}\n"  # todo :  make compadible with multiplycations
        return varNameB

    elif (varNameB.startswith("␀") & (not varNameA.startswith("␀"))):

        if varNameB[1:] == "0":
            return varNameA

        scoreTable += prefix + f"scoreboard players add #_mdb{varNameA} _mdb_{orgin} {varNameB[1:]}\n"

        return varNameA
    elif (varNameB.startswith("␀") & varNameA.startswith("␀")):

        va1 = setScore("_calcv_om1" + varNameA[1:], varNameA[1:])
        va1combined = addAToBO(va1, varNameB, operation, masterOrgin=masterOrgin)
        # scoreTable += f"scoreboard players operation #_mdb{va1} _mdb_{orgin} {operation}={varNameB[1:]}\n"
        return va1combined
    if (type(varNameA) != int):

        if not varNameA.startswith("_calcv"):
            vu = varNameA.split(".", 2)
            if len(vu) < 2:
                if vu[0] not in idToOrginRegister:
                    vu += [masterOrgin]  # works
                else:
                    vu += [orgin]
            else:
                vu = vu[::-1]
            orgin = vu[1]

    if (type(varNameB) != int):

        if not varNameB.startswith("_calcv"):
            vu = varNameB.split(".", 2)
            if len(vu) < 2:
                if vu[0] not in idToOrginRegister:
                    vu += [masterOrgin]  # works
                else:
                    vu += [orginb]
            else:
                vu = vu[::-1]
            orginb = vu[1]

    scoreTable += prefix + f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= #_mdb{varNameB} _mdb_{orginb}\n"
    return varNameA


def addValToA(varNameA, value, operation, orgin="core__calc"):  # the orgin is the function

    global scoreTable
    scoreTable += prefix + f"scoreboard players operation #_mdb{varNameA} _mdb_{orgin} {operation}= {value}"
    return varNameA


def resetCalcReg():
    global scoreTable
    scoreTable += prefix + "scoreboard players reset * _mdb_core__calc\n"


scoreTable = ""
prefix = ""


def functify_aquasion(varname, equation, orgi, prefix0=""):
    global scoreTable, prefix, allreadySettoNull, idToOrginRegister
    idToOrginRegister = {}
    allreadySettoNull = []
    scoreTable = ""
    if prefix0 != "":
        prefix = prefix0 + " "

    result = parse_expression("0+" + equation)

    def calc(r, n=0, literal="a", orginU=""):
        # print(r)
        global scoreTable
        op, v1, v2 = r
        # print(r)
        ori = "core__calc"
        orib = "core__calc"
        stack = []
        v1IsOtherVar = False
        v2IsOtherVar = False

        if (type(v1) != int) & (type(v1) != list):

            if not v1.startswith("#_mdb"):
                v1IsOtherVar = True


        if (type(v2) != int) & (type(v2) != list):
            if not v2.startswith("#_mdb"):

                orib = orgi
                v2IsOtherVar = True
        if type(v1) == list:
            v1, fuc = calc(v1, n + 1, literal="a")
            stack += [fuc]

        if type(v2) == list:
            v2, fuc2 = calc(v2, n + 1, literal="b")
            stack += [fuc2]
        if type(v1) == int:
            v1 = str(v1)
            # print(v1, v1.isdigit())
            if v1.isdigit():

                v1 = setScore(str(n) + literal, v1)

                # v1 = "␀" + str(v1)

        if type(v2) == int:
            v2 = str(v2)

            if v2.isdigit():
                v2 = setScore(str(n) + literal + "1", v2, )
                # v2 = "␀" + str(v2)

        if v1IsOtherVar:
            vu = v1.split(".", 2)
            if len(vu) < 2:
                vu += [orgi]  # works
            else:
                vu = vu[::-1]
            n1v = setScore("_calcv1store" + str(random.randint(0, 999990)), 0)
            v2 = addAToBO(n1v, vu[0], "+", orginb=vu[1], masterOrgin=orgi)
            ori = orgi

        if v2IsOtherVar:
            vu2 = v2.split(".", 2)
            if len(vu2) < 2:
                vu2 += [orgi]  # works
            else:
                vu2 = vu2[::-1]
            n2v = setScore("_calcv2store" + str(random.randint(0, 999990)), 0)

            v2 = addAToBO(n2v, vu2[0], "+", orginb=vu2[1], masterOrgin=orgi)
            orib = orgi


        # scoreTable+=f"--{v1}   {v2} |  {ori} . {orib} \n"
        match op:
            case "Add":

                v = addAToBO(v1, v2, "+", ori, orib, orgi)

            case "Mult":
                v = addAToBO(v1, v2, "*", ori, orib, orgi)
            case "Sub":
                v = addAToBO(v1, v2, "-", ori, orib, orgi)
            case "Div":
                v = addAToBO(v1, v2, "/", ori, orib, orgi)

        return v, stack

    vui = varname.split(".", 1)
    if len(vui) >= 2:
        orgi = vui[0]
        varname = vui[1]
    setScore(varname, 0, orgi)
    addAToBO(varname, calc(result, 0, "a", orgi)[0], "", orgi, masterOrgin=orgi)

    resetCalcReg()


def pr_outVar(varname, func):
    vu = varname.split(".", 2)
    if len(vu) < 2:
        vu += [func]
    else:
        vu = vu[::-1]
    return 'tellraw @p [{"text":"' + vu[1] + ': ","color":"gold"},{"text":"","color":"red"},{"score":{"name":"#_mdb' + \
        vu[1] + '","objective":"_mdb_' + vu[0] + '"}}]\n'


"""equation = '0+test'
functify_aquasion("varname",equation,"testfunction")
print("fdw",scoreTable,"--")
"""
