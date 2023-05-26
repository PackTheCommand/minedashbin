import tkinter
from tkinter import Text

from .independentComponents import createImage


class SugestionsBox(Text):
    def __init__(self,matchCollor,imgtypes=None,window=None,**kwargs):
        super().__init__(height=1,width=1,**kwargs)
        self.tag_configure("match",foreground=matchCollor)
        self.bind()
        self.tag_configure("mark",background="green")
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
        a2 = f"{self.selected}.end"
        self.tag_add("mark", a1,a2)
    def up(self,e):

        if self.selected ==1:
            return
        self.selected -= 1
        self.tag_remove("mark", "0.0", tkinter.END)
        a1 = f"{self.selected}.0"
        a2 = f"{self.selected}.end"
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
        c=createImage(self.imgTypes[type0], 14, 14, name="defuld_sugestion",master=self.w)
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

"""tk= tkinter.Tk()

b=boxText("#ff00ff")
b.pack()
b.addItem("hello","world")
b.addItem("hello","world")
b.addItem("hello","world")

tk.mainloop()"""
