import json
import os
import sys

class Settings:
    def __init__(self, path):
        self.path = path
        try:
            with open(path, "r") as f:
                jl=json.load(f)
                if len(jl)==0:
                    raise FileNotFoundError
                self.settings = jl[0]
                if self.settings=={}or self.settings==None:
                    raise FileNotFoundError
        except FileNotFoundError:
            print("No setting.json found using default settings")
            self.settings = {"AllPlugins": {}}
            self.save()
            self.save()

        self.defuldOptions={}



    def save(self):
        with open(self.path, "w") as f:
            json.dump([self.settings], f)
    def addToExistingSetting(self,key,value):
        try:
            self.settings[key] +=value
            return True
        except Exception:
            pass
        return False

    def removeFromExistingSetting(self,key,value):
        try:
            self.settings[key].remove(value)
            return True
        except Exception:
            pass
        return False
    def get(self, key):
        try:
            return self.settings[key]
        except KeyError:
            try:
                return self.defuldOptions[key]
            except KeyError:
                pass
                print(self.settings)
                print("Unknown Seting",key)
                return None

    def set(self, key, value):
        try:
            self.settings[key] = value
            return True
        except Exception:
            pass
        return False

    def delete(self, key):
        try:
            self.settings.pop(key)
            return True
        except Exception:
            pass
        return False
import modernApi
import plugins.multiplayer.multiplayer
class Plugin:
    def __init__(self,name):
        self.name = name
        import modernApi as ma
        self.API=ma
        self.path ="/plugins/"
        self.imported=None
        self.absolutepath=__file__[::-1].split("\\",1)[1][::-1]
        try:
            sys.path.insert(0, self.absolutepath + rf"\plugins\\{self.name}\\")
            self.imported=__import__(f"{self.name}")
        except NotImplementedError:
            raise Exception("PluginLoader ERROR - plg-name : "+name)
    def initilize(self):
        if self.imported==None:
            raise Exception(f"Plugin Initialization ERROR - unable to initialize unloaded plugin '{self.name}'")
        try:
            self.imported.init(self.API)
        except AttributeError:
            print(repr(self.imported.multiplayer.multiplayer.init()))
            raise Exception(f"Plugin Initialization ERROR - plugin '{self.name}' missing init()")


ps=Settings(path="plugins/plugins.spec")
def load_plugins():

    alplgs=ps.get("AllPlugins")
    for key in alplgs.keys():
        plugin=Plugin(alplgs[key]["name"])
        plugin.initilize()

def addPlugin(name,vers=0.0,author="Unknown"):
    ps.get("AllPlugins")[name]={"name":name,"vers":vers,"author":author, "disabled": False, "state": "Null", "preInstall": False}
    ps.save()
    print(ps.get("AllPlugins"))

load_plugins()

