import json


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
            self.settings = {"All-Projects":{},"Current-Project":None,"pr_ids":[]}
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