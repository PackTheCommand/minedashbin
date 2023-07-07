import json
import os
import sys

cache={"pre-kww-analysis":[],"pre-op-identific":[],"pre-func-grouping":[],"pre-mine-formatting":[],"post-processing":[]}
def cache_extentions(extentions:list,com_version,paser):
    for ext in extentions:

        with open("extentions/"+ext+"/.spec") as f:
            metadata=json.load(f)




        sys.path.insert(0,"extentions")
        imp=__import__(ext)

        try:
            imp.setup(com_version,{"version":"???-beta","target":"1.19/1.20"})
        except IOError:
            print(ext,"provides no function Setup")
            continue





        if metadata["hook-point"] in cache.keys():
           cache[metadata["hook-point"]]+=[imp]
        else:
            print("Unrecognized processing step")


def execute_extentions(step,paser):
    for ext in cache[step]:
        ext.service(paser)


cache_extentions(["loof"],"19.4",None)