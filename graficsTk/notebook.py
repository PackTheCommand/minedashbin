import tkinter
from tkinter import Frame, Label

from graficsTk import Collor, createLabel1


class swithchFrame(Frame):
    def __init__(self,master=None,**kwwargs):
        Frame.__init__(self,master=master,**kwwargs)
        self.currantFrame=None
        self.framestack=[]
        self.pointer=0
    def setFrame(self,frame,parms):
        frame.pack(parms)


    def navigateF(self):
        if self.pointer <len(self.framestack):
            self.pointer+=1
        else:
            return
        if self.currantFrame:
            self.currantFrame.pack_forget()
        self.currantFrame = self.framestack[self.pointer]
        self.currantFrame.pack(fill="both", expand=True,in_=self)
    def navigateB(self):
        if self.pointer>=0:
            self.pointer-=1
        else:
            return
        if self.currantFrame:
            self.currantFrame.pack_forget()
        self.currantFrame=self.framestack[self.pointer]
        self.currantFrame.pack(fill="both",expand=True)
    def puschFrame(self,frame):
        self.framestack.append(frame)



        #self.currantFrame=frame

        return len(self.framestack)-1
        #self.currantFrame.pack(fill="both", expand=True)
    def show(self,index):
        self.pointer=index
        print("c",self.currantFrame)
        if self.currantFrame!=None:
            print("forgot",self.currantFrame)
            self.currantFrame.pack_forget()
        self.currantFrame=self.framestack[index]
        self.currantFrame.pack(fill="both",expand=True)


class TabBook(Frame):
    def __init__(self,title="Tabs",**kwargs):
        Frame.__init__(self,**kwargs)
        self.labels={}
        self.oncloses={}
        self.labelFrame=Frame(master=self,bg=Collor.bg)
        self.labelFrame.pack(fill="x")
        self.firstButton=None
        self.showFsw=swithchFrame(master=self,bg=Collor.bg)
        print("showF",self.showFsw)
        self.__selected_indicator=None
        self.showFsw.pack(side="bottom")
        self.labelFont=tkinter.font.Font(size=12,family="Calibre")
        c1 = createLabel1(self.labelFrame, title, font=self.labelFont)
        c1.pack(side="left")
        cp1 = Label(self.labelFrame, text="", font=self.labelFont,bg=Collor.bg_lighter,width=0)
        cp1.pack(side="left")
        self.expanded=False
        def shrinkGrow(e):
            if self.expanded:
                self.showFsw.currantFrame.pack_forget()
                return

        c1.bind("<Button-1>",shrinkGrow)
    def getMaster(self):
        return self.showFsw
    def gm(self):
        return self.showFsw
    def addButton(self,text,id,command):
        f = Frame(master=self.labelFrame, bg=Collor.bg)
        l = Label(master=f, text=text, fg=Collor.fg, bg=Collor.bg, font=self.labelFont)

        l.pack(side="left", padx=(4, 0))
        f.pack(side="left", padx=(1, 1))

        def enter():
            f.configure(bg=Collor.bg_lighter)
            l.configure(bg=Collor.bg_lighter)


        def leave():
            f.configure(bg=Collor.bg)
            l.configure(bg=Collor.bg)


        f.bind("<Enter>", lambda u: enter())
        f.bind("<Leave>", lambda u: leave())


        l.bind("<Button-1>", lambda e: command(id))
        if not self.firstButton:
            self.firstButton=f
    def addTabLabel(self,text,id4):
        f=Frame(master=self.labelFrame,bg=Collor.bg)
        l=Label(master=f,text=text,fg=Collor.fg,bg=Collor.bg,font=self.labelFont)
        fm = Frame(master=f, bg=Collor.bg,height=3)
        fm.pack(side="bottom",fill="x")
        close=Label(master=f,text="✖",bg=Collor.bg,fg=Collor.fg)
        l.pack(side="left",padx=(4,0))
        if self.firstButton:
            f.pack(side="left",padx=(1,1),before=self.firstButton)
        else:
            f.pack(side="left", padx=(1, 1))
        def enter():
            f.configure(bg=Collor.bg_lighter)
            l.configure(bg=Collor.bg_lighter)
            close.configure(bg=Collor.bg_lighter)
        def leave():
            f.configure(bg=Collor.bg)
            l.configure(bg=Collor.bg)
            close.configure(bg=Collor.bg)


        f.bind("<Enter>",lambda u:enter())
        f.bind("<Leave>", lambda u:leave() )
        close.pack(side="left",padx=(2,0))
        def nav(fr):
            self.nav(id4)


            print("selected fdsfdsfdsa")

        l.bind("<Button-1>",lambda e,fr_=fm:nav(fr_))
        close.bind("<Button-1>", lambda e,s=self: s.destroyTab(id4))

        self.labels[id4]=(f,l,fm)
    def addTab(self,name,frame:tkinter.Widget,onClose=None):

        ind=self.showFsw.puschFrame(frame)
        self.oncloses[ind]=onClose

        self.addTabLabel(name,ind)
        return ind
    def destroyTab(self,id):
        close=self.oncloses[id]
        f,l,indic=self.labels[id]
        f.pack_forget()
        if close:
            close()
    def nav(self,index):
        self.expanded=True
        def select(fr):
            if self.__selected_indicator:
                self.__selected_indicator.configure(bg=Collor.bg)
            self.__selected_indicator=fr
            fr.configure(bg=Collor.selector_is)

        f, l, indic = self.labels[index]

        select(indic)
        print(self,self.showFsw)
        self.showFsw.show(index)

