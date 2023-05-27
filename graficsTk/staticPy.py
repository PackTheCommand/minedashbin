import json


Year,Month,Day=2000,1,1
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


Seti = Settings("../settings.json")
mode = Seti.get("mode")


class Collor():
    ChatBuble="#175676"
    transparency_color ="#ff00f2"
    Error="#D7263D"
    Warn="#FFB800"
    Attention= "#E4FF1A"
    Success= "#44AF69"#6EEB83
    Neutral= "#1BE7FF"
    Ice="#1B98E0"

    Polar="#E8F1F2"

    if mode == "dark":
        bg = "#232327"
        bg_darker = "#151517"
        fg = "#c0c0c0"
        highlight="#2B9EB3"
        info = "#157145"
        bg_lighter="#515151"
        fg_inverted = "#161616"
        selector_none="#2A6780"
        bg_light_l1="#797979"
        selector_is="#247BA0"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        bg_selected = "#80868a"
        fg_reinst = "#181818"
        err_color = "#AA1F2B"
    elif mode == "dark-red":
        bg = "#232327"
        bg_darker = "#151517"
        fg = "#D7CACD"
        bg_light_l1 = "#797979"
        highlight = "#F15152"
        info = "#157145"
        bg_lighter = "#515151"
        fg_inverted = "#161616"
        selector_none = "#81171B"
        selector_is = "#AD2E24"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        bg_selected = "#80868a"
        fg_reinst = "#181818"
        err_color = "#AA1F2B"
    elif mode == "dark-emerald":
        bg = "#232327"
        bg_darker = "#151517"
        fg = "#E1F2FE"
        bg_light_l1 = "#797979"
        highlight = "#23CE6B"
        info = "#157145"
        bg_lighter = "#515151"
        fg_inverted = "#161616"
        selector_none = "#297045"
        selector_is = "#3BC14A"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        bg_selected = "#80868a"
        fg_reinst = "#181818"
        err_color = "#AA1F2B"


    else:
        bg = "#E0E0E0"
        bg_darker = "#94999c"
        fg = "#161616"
        fg_inverted = "silver"
        bg_cancel = bg
        bg_light_l1 = "#797979"
        bg_lighter=bg
        info = "#157145"
        highlight = "#2B9EB3"
        bg_selected = "#505457"
        bg_reinst = "#CECECE"
        fg_reinst = "#B5B5B5"
        err_color = "#FF4460"
        selector_none = "#c2c2c2"
        selector_is = "#e2e2e2"