import json
import os
import sys

from minedashbin import exeptions_

funcNames={"after-brackify":"service_brackify","pre-kww-analysis":"service_kww_analysis","pre-op-identific":"service_op_analysis","pre-func-grouping":"service_func_group","pre-mine-formatting":"service_mine_format","pre-saving":"service_pre_saving",}
cache={"after-brackify":[],"pre-kww-analysis":[],"pre-op-identific":[],"pre-func-grouping":[],"pre-mine-formatting":[],"pre-saving":[]}
def cache_extentions(extentions:list,com_version,paser):
    for ext in extentions:
        if not os.path.exists("extentions/"+ext+"/.spec"):
            exeptions_.ex("extention not found: "+ext)

        with open("extentions/"+ext+"/.spec") as f:
            metadata=json.load(f)




        sys.path.insert(0,"extentions")
        imp=__import__(ext)

        try:
            imp.setup(com_version,{"version":"???-beta","target":"1.19/1.20"})
        except IOError:
            print(ext,"provides no function Setup")
            continue




        for testkey in metadata["hook-points"]:
            if testkey in cache.keys():
                cache[testkey]+=[imp]
            else:
                print("Unrecognized processing step: ",testkey)


def execute_extentions(step,paser):
    for ext in cache[step]:
        try:
            exec("ext."+funcNames[step]+"(paser)")
        except EOFError: exeptions_.ex(f"Extention '{ext.__name__}' doesn't provide service for event '{step}' \u001b[37m")



