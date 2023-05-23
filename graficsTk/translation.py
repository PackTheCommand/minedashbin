import json

def getPath():
    f = str(__file__)
    fs = f[::-1].split("\\", 1)[1]
    return fs[::-1]
absolutePath = getPath()
class Translation():
    def __init__(self,lang,folderpath="" ,*args, **kwargs):
        # how this black magic works here=>
        # https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
        super( Translation, self).__init__(*args, **kwargs)
        self.dict = {}
        self.lang = lang
        self.folderpath = folderpath
        self.load_Language()
    def load_Language(self):
        self.dict.clear()
        with open(absolutePath+"\\lang\\"+self.lang+".lang.json") as f:
            tran=json.load(f)[0]
            for key in tran.keys():
                self.dict[key]=tran[key]

    def get(self, item):
        if item in self.dict.keys():
            return self.dict[item]
        else:
            return self.lang+"."+str(item)


