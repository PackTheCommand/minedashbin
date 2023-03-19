import json


class Settings:
    def __init__(self, path):
        self.path = path
        try:
            with open(path, "r") as f:

                self.settings = json.load(f)[0]
        except FileNotFoundError:
            print("No setting.json found using default settings")
            self.settings = {"mode": "dark",}
            self.save()

        self.defuldOptions={"mode": "dark","noInfoText":False,"devMode":False,"$638382%Cheats":False}



    def save(self):
        with open(self.path, "w") as f:
            json.dump([self.settings], f)

    def get(self, key):
        try:
            return self.settings[key]
        except KeyError:
            try:
                return self.defuldOptions[key]
            except KeyError:
                pass
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