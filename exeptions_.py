def BrackedNeverClosed(l):
    print("Err: The bracked in line "+str(l)+" was never closed")
    ex()
def MissingBrackts(l):
    print("Err: EmptyFunction in line "+str(l))
    ex()
def MissingSimicolon(l):
    print("Err: Missing semicolon in line "+str(l))
    ex()
def ex()->exit:
    exit(404)

def CompilationError(pycode):
    print(f"Err: CompilationError '{repr(pycode)}' [Compiler-fails] reason <seePyBasedError> ")
    ex()


def unknownOperator(op,l):

    print(f"Err: Unknown operator '{op}' [Compiler-fails] in line "+str(l))
    ex()


def indexiationError(op, l):
    print(f"Err: line '{op}' has forbiden spacing number schould be '  '")
    ex()


def TypeValueError(l):
    print("Err: TypeValueError in line "+str(l))
    ex()

def kww_missing_arguments(l,kww,got,takes):
    print(f"Err: Keyword '{kww}' is arguments not matching given:{got} needs:{takes}")
    ex()


def parameterLimitReched(l):
    print("Err: ParameterLimitRecheched in line "+str(l)+" not more than 9999 parameters are alowed")
    ex()
def parameterCountNotMacking(func,takes,got):
    print(f"Err: Parameters of function {func} not matching with required params given:{got} needs:{takes}")
    ex()

def ccFileError(addI,file):
    print("Err: CCFileError triing to load "+str(file) + " "+addI)
    ex()
def functionDoesntExist(func):
    print(f"Err: function '{func}' doesn't exist")
    ex()
def nativeModulerNotFound(modulepath):
    print(f"Err: Native-Module {modulepath} not found")
    ex()
def schortGivenToMuchArgs(synt):
    print(f"Err: Short needs two arguments providet: {synt} ")
    ex()
def ModuleNotFound(modulepath):
    print(f"Err: Module {modulepath} not found")
    ex()