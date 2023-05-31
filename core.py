
"""
def EVAL_VAR_INSTRUCKTION(inst):
    body=[]
    curantVarnem=""
    head=""
    instucktion="+"
    target=0


    def addtobody():
        nonlocal instucktion,body,curantVarnem

        body += [(instucktion, curantVarnem)]

        pass

        curantVarnem, instucktion = "", ""
    for a in inst:
        if target==0:
            if a==" ":
                continue
            if a=="=":
                target=1


            head+=a
        else:
            if a==" ":
                continue
            if a in ["*","/","+","-"]:
                if instucktion:
                    addtobody()
                instucktion=a
                continue
            else:
                if a==" ":
                    print("skipp")
                    continue
            curantVarnem+=a
    if bool(curantVarnem)&bool(instucktion):
        addtobody()
    return head,body



def groupInstrucktions(items=[("+",1)]):
    for inst,e in items:
        """
import ast


def EVAL_VAR_INSTRUCKTION(code):



    def evaluate_expression(expression):
        if isinstance(expression, ast.Num):
            print(expression.n)  # Print numeric value
        elif isinstance(expression, ast.BinOp):
            left = evaluate_expression(expression.left)
            right = evaluate_expression(expression.right)
            if isinstance(expression.op, ast.Add):
                return left + right
            elif isinstance(expression.op, ast.Sub):
                return left - right
            elif isinstance(expression.op, ast.Mult):
                return left * right
            elif isinstance(expression.op, ast.Div):
                return left / right
        elif isinstance(expression, ast.Name):
            # Handle variable references
            return expression.id
        else:
            raise NotImplementedError("Expression type not supported")

        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr):
                evaluate_expression(node.value)

print(EVAL_VAR_INSTRUCKTION("test=3"))



class CalcRegister:
    @staticmethod
    def coppyToRegister(varNameA,orginA,varNameB,orginB): # the orgin is the function
        return f"scoreboard players operation #coreA __mbd__core__calc = #_mdb{varNameA} _mdb_{orginA}\n"\
               f"scoreboard players operation #coreB __mbd__core__calc = #_mdb{varNameB} _mdb_{orginB}\n"

    @staticmethod
    def fluschRegister():
        return f"scoreboard players set #coreA __mbd__core__calc 0\n" \
               f"scoreboard players set #coreB __mbd__core__calc 0\n"

    @staticmethod
    def calculate(operation): # the orgin is the function
        return f"scoreboard players operation #coreA __mbd__core__calc {operation}= #coreB __mbd__core__calc\n"

    @staticmethod
    def dumpIntoScoreboard(varName,orgin):
        return f"scoreboard players operation #_mdb{varName} _mdb_{orgin} = #coreA __mbd__core__calc\n"


def addAToB(varNameA, orginA, varNameB, orginB):  # the orgin is the function
    return f"scoreboard players operation #coreA __mbd__core__calc += #_mdb{varNameA} _mdb_{orginA}\n" \
           f"scoreboard players operation #coreB __mbd__core__calc = #_mdb{varNameB} _mdb_{orginB}\n"