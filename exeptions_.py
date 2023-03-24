
def ex()->exit:
    exit(404)

def unknownOperator(op,l):

    print(f"Err (C:001): Unknown operator '{op}' [Compiler-fails] in line "+str(l))
    ex()
def unableToUnderstandInstrucktion(op,l):

    print(f"Err (C:002): Unknown Instruction '{op}' [Compiler-fails] in line "+str(l))
    ex()

def indexiationError(op, l):
    print(f"Err (C:003): line '{op}' has forbiden spacing number schould be '  '")
    ex()


def TypeValueError(l):
    print("Err (C:004): TypeValueError in line "+str(l))
    ex()

def kww_missing_arguments(l,kww,got,takes):
    print(f"Err (C:005): Keyword '{kww}' is arguments not matching given:{got} needs:{takes}")
    ex()


def parameterLimitReched(l):
    print("Err (C:006): ParameterLimitRecheched in line "+str(l)+" not more than 9999 parameters are alowed")
    ex()
def parameterCountNotMacking(func,takes,got):
    print(f"Err (C:007): Parameters of function {func} not matching with required params given:{got} needs:{takes}")
    ex()

def ccFileError(addI,file):
    print("Err (C:008): CCFileError triing to load "+str(file) + " "+addI)
    ex()
def functionDoesntExist(func):
    print(f"Err (C:009): function '{func}' doesn't exist")
    ex()
def nativeModulerNotFound(modulepath):
    print(f"Err (C:011): Native-Module {modulepath} not found")
    ex()
def schortGivenToMuchArgs(synt):
    print(f"Err (C:012): Short needs two arguments providet: {synt} ")
    ex()
def ModuleNotFound(modulepath):
    print(f"Err (C:013): Module {modulepath} not found")
    ex()

def StringNeverClosedErr(line):
    print(f"Err (C:014): String never closed in line '{line}'")
    ex()
def MissingBrackts(l):
    print("Err (C:015): EmptyFunction in line "+str(l))
    ex()
def MissingSimicolon(l):
    print("Err (C:016): Missing semicolon in line "+str(l))
    ex()


def CompilationError(pycode):
    print(f"Err (C:017): CompilationError '{repr(pycode)}' [Compiler-fails] reason <seePyBasedError> ")
    ex()
def BrackedNeverClosed(l):
    print("Err (C:018): The bracked in line "+str(l)+" was never closed")
    ex()