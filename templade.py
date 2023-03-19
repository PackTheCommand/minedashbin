def getIncludeblock(name,block):
        fblock=""
        for it in block:
            fblock+=""+it+"\n"


        return f"section {name}\n" \
                "\n" \
               f"{fblock}\n" \
                "\n"


def getFuncTemplate(name,count,args):
    argsS=""
    for a in args:
        argsS+=a+" "



    return f"# {name} {count} {argsS}\n"


