

def setup(com_version,meta):
    """
    gets called on initilization
    """
    pass
def service_mine_format(paserObject):
    for bl in paserObject.blocks["cutouts"]:

        blockl="inject "
        def ins(string):
            nonlocal blockl
            blockl+=string+"\n"
        try:
            exec(paserObject.blocks["cutouts"][bl][:-2])
        except Exception:
            blockl="say minedashbin//Error:: pythonic-code execution generation error"
            print("Error trying to execute pythonic code")
        paserObject.shorts[bl]=blockl



    print(vars(paserObject))
    """
    Main processing here

    :param paserObject:
    :return:
    """
