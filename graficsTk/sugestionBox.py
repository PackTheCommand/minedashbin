import tkinter
from tkinter import Text

from . import Collor
from .independentComponents import createImage, createLabel1


class SugestionsBox(Text):
    def __init__(self,matchCollor,selectCollor,imgtypes=None,window=None,**kwargs):
        super().__init__(height=1,width=1,**kwargs)
        self.tag_configure("match",foreground=matchCollor)
        self.bind()
        self.tag_configure("mark",background=selectCollor)
        self.items=0
        self.w=window
        if imgtypes==None:
            imgtypes={}
        self.imgTypes=imgtypes

        self.selected=0
        self.itemsl=[]
        self.bind("<Down>",self.down)

        self.bind("<Up>", self.up)

    def getSelected(self):
        if len(self.itemsl)==0:
            return ""
        if self.selected==0:
            return self.itemsl[0]
        return self.itemsl[self.selected-1]
    def down(self,e):
        print(self.selected)

        if self.selected>=self.items:
            return
        self.selected += 1
        self.tag_remove("mark", "0.0", tkinter.END)
        a1 = f"{self.selected}.0"
        a2 = f"{self.selected+1}.0"
        self.tag_add("mark", a1,a2)
    def up(self,e):

        if self.selected ==1:
            return
        self.selected -= 1
        self.tag_remove("mark", "0.0", tkinter.END)
        a1 = f"{self.selected}.0"
        a2 = f"{self.selected+1}.0"
        self.tag_add("mark", a1,a2)
    def br(self):
        return "break"

    def addItem(self,texta,textb,type0="default"):
        self["state"]="normal"
        self.items+=1


        a1 = f"{self.items}.0"
        a2 = f"{self.items}.{len(texta)+1}"

        self.insert(a1," "+texta,)
        self.insert( tkinter.END,textb+"\n",)
        self.tag_add("match",a1,a2)
        c=createImage(self.imgTypes[type0], 18, 18, name="defuld_sugestion_"+self.imgTypes[type0],master=self.w)
        print(tkinter.image_names())

        self.image_create(a1, image=c)
        self["state"] = "disabled"

        self.configure(height=self.items)
        self.itemsl+=[texta+textb]
        if len(self.itemsl)>=2:
            maxa=len(max(self.itemsl,key=len))+5
            print(type(maxa))
            self.configure(width=maxa)
        else:
            self.configure(width=len(self.itemsl[0])+4)
    def clear(self):
        self.items=0
        self.itemsl.clear()
        self.selected=0
        self["state"] = "normal"
        self.replace("0.0",tkinter.END,"")
        self["state"] = "disabled"


class PathShow(tkinter.Frame):
    def __init__(self,activeColor,inactivecolor,**kwargs):
        super().__init__(**kwargs)
        self.labels = []
        self.activecolor = activeColor
        self.inactivecolor = inactivecolor

    def cl(self, name):
        l = createLabel1(self, name, bg=self.inactivecolor)
        l.pack(side="left")

        self.labels += [l]

        def enter():
            l.configure(bg=self.activecolor,fg=Collor.Polar)

        def leave():
            l.configure(bg=self.inactivecolor,fg=Collor.fg)

        l.bind("<Enter>", lambda u: enter())
        l.bind("<Leave>", lambda u: leave())

    def adddecorator(self, symbol):
        l = createLabel1(self, symbol, bg=self.inactivecolor)
        l.pack(side="left")

        self.labels += [l]

    def delall(self):
        for e in self.labels:
            e.destroy()
"""tk= tkinter.Tk()

b=boxText("#ff00ff")
b.pack()
b.addItem("hello","world")
b.addItem("hello","world")
b.addItem("hello","world")

tk.mainloop()"""
