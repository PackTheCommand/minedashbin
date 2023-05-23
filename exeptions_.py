
def ex()->exit:
    exit(404)



class throwError:
    @staticmethod
    def unknownOperator(op, l):
        print(f"Err (C:001): Unknown operator '{op}' [Compiler-fails] in line " + str(l))
        ex()

    @staticmethod
    def unableToUnderstandInstrucktion(op, l):
        print(f"Err (C:002): Unknown Instruction '{op}' [Compiler-fails] in line " + str(l))
        ex()

    @staticmethod
    def indexiationError(op, l):
        print(f"Err (C:003): line '{op}' has forbiden spacing number schould be '  '")
        ex()

    @staticmethod
    def TypeValueError(l):
        print("Err (C:004): TypeValueError in line " + str(l))
        ex()

    @staticmethod
    def kww_missing_arguments(l, kww, got, takes):
        print(f"Err (C:005): Keyword '{kww}' is arguments not matching given:{got} needs:{takes}")
        ex()

    @staticmethod
    def parameterLimitReched(l):
        print("Err (C:006): ParameterLimitRecheched in line " + str(l) + " not more than 9999 parameters are alowed")
        ex()

    @staticmethod
    def parameterCountNotMacking(func, takes, got):
        print(f"Err (C:007): Parameters of function {func} not matching with required params given:{got} needs:{takes}")
        ex()

    @staticmethod
    def ccFileError(addI, file):
        print("Err (C:008): CCFileError triing to load " + str(file) + " " + addI)
        ex()

    @staticmethod
    def functionDoesntExist(func):
        print(f"Err (C:009): function '{func}' doesn't exist")
        ex()

    @staticmethod
    def nativeModulerNotFound(modulepath):
        print(f"Err (C:011): Native-Module {modulepath} not found")
        ex()

    @staticmethod
    def schortGivenToMuchArgs(synt):
        print(f"Err (C:012): Short needs two arguments providet: {synt} ")
        ex()

    @staticmethod
    def ModuleNotFound(modulepath):
        print(f"Err (C:013): Module {modulepath} not found")
        ex()

    @staticmethod
    def StringNeverClosedErr(line):
        print(f"Err (C:014): String never closed in line '{line}'")
        ex()

    @staticmethod
    def MissingBrackts(l):
        print("Err (C:015): EmptyFunction in line " + str(l))
        ex()

    @staticmethod
    def MissingSimicolon(l):
        print("Err (C:016): Missing semicolon in line " + str(l))
        ex()

    @staticmethod
    def CompilationError(pycode):
        print(f"Err (C:017): CompilationError '{repr(pycode)}' [Compiler-fails] reason <seePyBasedError> ")
        ex()

    @staticmethod
    def BrackedNeverClosed(l):
        print("Err (C:018): The bracked in line " + str(l) + " was never closed")
        ex()

    @staticmethod
    def invalidIfinstucktion(func):
        print(f"Err (C:0019): invalid if instruction '{func}' ")
        ex()

    @staticmethod
    def variableNotdeclarated_Error(var):
        print(f"Err (C:020): Variable was never initialized '{var}' ")
        ex()

    @staticmethod
    def functionforseduenotdefined(name,case):
        print(f"Err (C:021): {case}-seduce function '{name}' has never been declared")
        ex()

    @staticmethod
    def unknownShort(sh):
        print(f"Err (C:022): Unknown Short '{sh}'  ")
        ex()

