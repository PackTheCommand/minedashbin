import copy
import glob
import os
import re
import tkinter
from fnmatch import fnmatch
from tkinter import Tk, Frame
from tkinter.ttk import Treeview, Style
from .staticPy import Collor
from .independentComponents import *



class FileTree(Treeview):
    def __init__(self,width=200,**kwargs):
        super(FileTree, self).__init__(show="tree",**kwargs,)
        s=Style(self)

        self.FileTreeIDReg={}
        self.column("#0", width=width, stretch=True,)
        s.theme_use("clam")
        s.configure("Treeview", background=Collor.bg, foreground=Collor.fg,font=tkfont.Font(size=20,family="Bahnschrift",weight="bold"),
                    rowheight=25,
                    fieldbackground=Collor.bg,
                    bordercolor=Collor.bg, lightcolor=Collor.bg,
                    darkcolor=Collor.bg)
        self.fp = __file__[::-1].split("\\", 1)[1][::-1]
        s.map("Treeview", background=[("selected",Collor.bg)], highlightcolor=[('focus', 'green'),('!focus', 'red')])
        self.folderImg = createImage(self.fp + r"\\resource\\folder_64.png", 16, 16, name="folder16")
        self.fileImg = createImage(self.fp + "\\resource\\file_64.png", 16, 16, name="file16")
        self.rootImg = createImage(self.fp + "\\resource\\root_path_64.png", 16, 16, name="root16")
        self.fileImgs={}
        self.fileIds={}
        self.idToMaster={}
        self.bigestId=0
        self.__opened_file=None
        self.coppied=""
        self.m=m = tkinter.Menu(bg=Collor.bg,fg=Collor.fg,borderwidth=0,bd=0,font=tkfont.Font(size=10))
        self.curantSel=0
        def delfile():

            path=getPathToId(self.curantSel)
            if path:
                print(path)
                self.delete(self.curantSel)
            pass
        def copyfile():
            path = getPathToId(self.curantSel)
            if path:
                print(path)

                self.coppied=path
            pass

            pass
        def pastefile():
            if self.coppied!="":

                self.ins("",self.idToMaster[self.bigestId-1],self.coppied.split("\\",)[-1],self.bigestId)
                self.bigestId+=1
            pass
        def cutfile():
            pass
        def setsel(u):
            def aftet():
                f=self.focus()
                self.curantSel=f

                if getPathToId(f):


                    print(getPathToId(f))
                    self.__opened_file=getPathToId(f)
                    self.event_generate("<<OpenFile>>")
            self.after(10,aftet)
        def getPathToId(id):
            if int(id) in self.fileIds:
                return self.fileIds[int(id)]
            print(id)
            return None

        def openfile(e=None):
            self.event_generate("<<OpenFile>>")
            pass
        self.bind("<Double-Button-1>",openfile)
        self.bind("<Button-1>", setsel)

        m.add_command(label="Open", command=openfile)
        m.add_command(label="Coppy", command=copyfile)
        m.add_command(label="Paste", command=pastefile)
        m.add_command(label="Cut", command=cutfile)

        m.add_command(label="Delete", command=delfile)

        def openMenu(e):
            nonlocal self


            self.m.tk_popup(e.x + self.winfo_x()+self.winfo_rootx(), e.y + self.winfo_y()+self.winfo_rooty())
            print(e,self.winfo_y())


        self.bind("<Button-3>", openMenu)

        for i in os.listdir(self.fp+r"\\resource\\fileExtentions"):
            if i.find(".")==-1:
                continue
            ext,type=i.split(".",1)
            ext=ext.replace("_64","")
            if type=="png":
                im=createImage(self.fp + "\\resource\\fileExtentions\\"+i, 20, 20, name="ext_"+ext)
                self.fileImgs[ext] = im

        pass

    def getFile(self):
        return self.__opened_file
    def ins(self, tree,ins: str, text: str, iid: int, fileInfo=("D", "C:\\"),type="file",open=False):
        global pages
        self.idToMaster[iid]=ins

        if type=="folder":
            return self.insert(ins, tkinter.END, text=text+str(iid), iid=iid , open=open,image= self.folderImg)
        elif type=="file":
            fextention=text.split(".")[-1]

            if fextention in  list(self.fileImgs.keys()):
                ico=self.fileImgs[fextention]
            elif fextention+"_64" in self.fileImgs.keys():
                ico = self.fileImgs[fextention+"_64"]
            else:
                ico=self.fileImg

            return self.insert(ins, tkinter.END, text=text, iid=iid, open=open,image= ico)
        elif type=="root":
            return self.insert(ins, tkinter.END, text=text, iid=iid, open=open,image= self.rootImg)


    def generateFileTree(self, dir):
        PROJECT_DIR=dir

        root = PROJECT_DIR
        idd_plus = 1
        dir_to_iid_list = {}

        globalDir = re.split("/" + "|" + r'\\', PROJECT_DIR)[-1]
        self.ins(self, "", globalDir, iid=0,type="root",open=True)

        dir_to_iid_list[PROJECT_DIR + "\\"] = (globalDir, 0)
        for path, subdirs, files in os.walk(root):

            path_splited = re.split("/" + "|" + r'\\', path)
            path_2 = copy.copy(path_splited)
            namePath = path_2.pop(-1)
            if (namePath == globalDir):
                continue
            masterPath = ""
            for s in path_2:
                masterPath += s + "\\"

            dir_to_iid_list[path + "\\"] = (path_splited[-1], idd_plus)

            path=self.ins(self, str(dir_to_iid_list[masterPath][1]),namePath, iid=idd_plus ,type="folder")
            idd_plus += 1




            idd_plus += 1
            pattern = "*"

        for path, subdirs, files in os.walk(root):

            for name in files:
                if fnmatch(name, pattern):
                    p = os.path.join(path, name)
                    # ps = re.split("/" + "|" + r'\\', path)
                    id=self.ins(self, str(dir_to_iid_list[path + "\\"][1]), name, iid=idd_plus ,type="file")
                    self.fileIds[idd_plus]=p
                    idd_plus += 1
        self.bigestId=idd_plus







