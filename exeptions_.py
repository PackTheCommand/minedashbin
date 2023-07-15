

disableEx=False
exeptionreson=""
def disableExit():
    global disableEx
    disableEx=True
def ex(errc):
    global exeptionreson
    print(u"\u001b[31m%s"% ((errc)))
    exeptionreson=errc
    if not disableEx:
        exit(404)
    raise Exception("Compilation Failed")




class throwError:
    @staticmethod
    def corupted_file(file, l):
        ex(f"Err (C:000): corrupted file '{file}' [Compiler-fails] in line " + str(l))

    @staticmethod
    def unknownOperator(op, l):
        ex(f"Err (C:001): Unknown operator '{op}' [Compiler-fails] in line " + str(l))


    @staticmethod
    def unableToUnderstandInstrucktion(op, l):
        ex(f"Err (C:002): Unknown Instruction '{op}' [Compiler-fails] in line " + str(l))


    @staticmethod
    def indexiationError(op, l):
        ex(f"Err (C:003): line '{op}' has forbiden spacing number schould be '  '")


    @staticmethod
    def TypeValueError(l):
        ex("Err (C:004): TypeValueError in line " + str(l))


    @staticmethod
    def kww_missing_arguments(l, kww, got, takes):
        ex(f"Err (C:005): Keyword '{kww}' is arguments not matching given:{got} needs:{takes}")


    @staticmethod
    def parameterLimitReched(l):
        ex("Err (C:006): ParameterLimitRecheched in line " + str(l) + " not more than 9999 parameters are alowed")


    @staticmethod
    def parameterCountNotMacking(func, takes, got):
        ex(f"Err (C:007): Parameters of function {func} not matching with required params given:{got} needs:{takes}")


    @staticmethod
    def ccFileError(addI, file):
        ex("Err (C:008): CCFileError triing to load " + str(file) + " " + addI)


    @staticmethod
    def functionDoesntExist(func):
        ex(f"Err (C:009): function '{func}' doesn't exist")


    @staticmethod
    def nativeModulerNotFound(modulepath):
        ex(f"Err (C:011): Native-Module {modulepath} not found")


    @staticmethod
    def schortGivenToMuchArgs(synt):
        ex(f"Err (C:012): Short needs two arguments providet: {synt} ")

    @staticmethod
    def ModuleNotFound(modulepath):
        ex(f"Err (C:013): Module {modulepath} not found")@staticmethod

    @staticmethod
    def StringNeverClosedErr(line):
        ex(f"Err (C:014): String never closed in line '{line}'")


    @staticmethod
    def MissingBrackts(l):
        ex("Err (C:015): EmptyFunction in line " + str(l))


    @staticmethod
    def MissingSimicolon(l):
        ex("Err (C:016): Missing semicolon in line " + str(l))


    @staticmethod
    def CompilationError(pycode):
        ex(f"Err (C:017): CompilationError '{repr(pycode)}' [Compiler-fails] reason <seePyBasedError> ")


    @staticmethod
    def BrackedNeverClosed(l):
        ex("Err (C:018): The bracked in line " + str(l) + " was never closed")


    @staticmethod
    def invalidIfinstucktion(func):
        ex(f"Err (C:0019): invalid if instruction '{func}' ")


    @staticmethod
    def variableNotdeclarated_Error(var):
        ex(f"Err (C:020): Variable was never initialized '{var}' ")


    @staticmethod
    def functionforseduenotdefined(name,case):
        ex(f"Err (C:021): {case}-seduce function '{name}' has never been declared")


    @staticmethod
    def unknownShort(sh):
        ex(f"Err (C:022): Unknown Short '{sh}'  ")

    @staticmethod
    def comversionNotInstaled(file):
        ex(f"Err (C:023): No commandset for version '{file}' installed ")
        pass

    @staticmethod
    def typeOverwriteError(var):
        ex(f"Err (C:024): typeOverwriteError '{var}' of type var can't be assigned to type function   ")
        pass



