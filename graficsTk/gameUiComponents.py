
from .staticPy import *

from .independentComponents import *



def crim(name):
    i = createImage("gresource/" + name + ".png", 30, 30)
    return i



class ButtonDroppDown(MovableFrame):
    def __init__(self,master:Window,disableX=False, width=380, height=320, highlightbackground="black", titel="", x=0, y=0,imagepath="",
                           disableDrag=False,
                           closeCommand=None):

        global thread
        MovableFrame.__init__(self, master=master, width=width, height=height, highlightbackground=highlightbackground,highlightcolor=Collor.selector_none,
                              highlightthickness=3, bd=0,
                              bg=Collor.bg)

        self.disableX=disableX
        self.disableDrag=disableDrag
        self.width=width
        self.height=height
        self.master=master
        self.closeCommand=closeCommand

        self.mFrame=mFrame=self

        mFrame.place(x=x, y=y, width=width, height=height)

        f = Frame(mFrame, bg=Collor.bg_darker)
        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        f.pack(side="top", anchor="n", fill="x")
        self.Label = LabelButton(master=f,img=imagepath).pack(side="left", anchor="nw")
        titel = L = Label(f, bg=Collor.bg_darker, fg=Collor.fg, font=font_size_medium, text=titel, anchor="w")
        self.MoveEvents=[]
        titel.pack(side="left", anchor="nw")
        if not self.disableDrag:
            self.make_draggable(titel, mFrame)
            self.make_draggable(f, mFrame)
        if not disableX:
            def close( frame):
                frame.place_forget()
                if self.closeCommand:
                    self.closeCommand()

            B = Button(f, text="❌", relief="flat", bg=Collor.bg_darker, fg=Collor.fg,
                       command=lambda: close( mFrame), border=0)
            B.pack(side="right", anchor="ne")

    def place_in_screen_window_rescue(self,widget):
        print("trigger",int(self.mFrame.place_info()["y"]))
        if int(self.mFrame.place_info()["y"])<0:
            print("fix")
            self.mFrame.place_configure(y=0)
        elif int(self.mFrame.place_info()["x"])<-self.width+80:
            print("fix")
            self.mFrame.place_configure(x=-self.width+80)

        elif int(self.mFrame.place_info()["x"])>self.master.winfo_width()-50:
            print("fix")
            self.mFrame.place_configure(x=self.master.winfo_width()-50)
        elif int(self.mFrame.place_info()["y"])>self.master.winfo_height()-40:
            print("fix")
            self.mFrame.place_configure(y=self.master.winfo_height()-40)
    def make_draggable(self,widget, toMoveWiget):
        widget.bind("<ButtonRelease-1>", lambda e: self.place_in_screen_window_rescue(widget))
        widget.bind("<Button-1>", lambda e: self.on_drag_start(e, widget, toMoveWiget))
        widget.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, widget, toMoveWiget))



    def on_drag_start(self,event, widget, tomove):

                widget._drag_start_x = event.x
                widget._drag_start_y = event.y
                tomove._drag_start_x = tomove.winfo_x()
                tomove._drag_start_y = tomove.winfo_y()
                tomove.last_xy=None


    def on_drag_motion(self,event, widget, tomove):

            x = tomove.winfo_x() - widget._drag_start_x + event.x
            y = tomove.winfo_y() - widget._drag_start_y + event.y
            if tomove.last_xy==None:
                tomove.last_xy=(x,y)

            if (not(tomove.last_xy[0]-20<x<tomove.last_xy[0]+20))|(not(tomove.last_xy[1]-20<y<tomove.last_xy[1]+20)):
                tomove.place(x=x, y=y)
            self.master.update_idletasks()


class ItemButton(Frame):
    def __init__(self,displayName,args=(),function=None,**kwargs):
        super().__init__(highlightthickness=1,bg=Collor.bg,highlightbackground=Collor.selector_none,**kwargs)
        nameMaxLen=16
        s=20
        L=LabelButton(master=self, img=createImage("../gresource/unknown_64.png", s, s)).pack(side="left")
        if len(displayName)>nameMaxLen:
            displayName=displayName[0:nameMaxLen+2]+"..."
        f=tkfont.Font(family="Bahnschrift",size=12)
        L=Label(master=self,text=displayName,width=20,font=f,bg=Collor.bg,fg=Collor.fg)
        L.pack(side="left",fill="x")
        self.bindLabel=L
        self.b=LabelButton(master=self, img=createImage("../gresource/cancel_64.png", s, s), command=self.pusch)
        self.b.pack(side="left")
        self.isAplied=False
        self.function=function
        self.args=args
    def pusch(self):
        self.isAplied=not self.isAplied
        self.setApplied(self.isAplied)
        if self.function:
            self.function(*self.args)


    def setApplied(self,tr):
        s = 20
        if tr:
            self.b.configure(image=createImage("../gresource/done_64.png", s, s))
        else:
            self.b.configure(image=createImage("../gresource/cancel_64.png", s, s))


class Table(Frame):
    def __init__(self,data=[],font=None,orientTop="col", **kwargs): #data contains in form [row->[>col in strings]] NAMES SCHOULD BE COL 0
        Frame.__init__(self,highlightthickness=2, bg=Collor.bg, highlightbackground=Collor.selector_none, **kwargs)
        self.columnconfigure(0,weight=len(data))
        self.rowconfigure(0,weight=200)
        def updateLable(lable:Label,value):
            lable.configure(text=str(value))

        for n,row in enumerate(data):
            #f=Frame()
            #f.pack(side="top",anchor="nw")

            for n2,col in enumerate(row):
                L=Label(master=self,font=font,bg=Collor.bg,fg=Collor.fg)
                if type(col)==Observable:
                    col.subscribe(lambda value:updateLable(L,value))
                    L.configure(text=str(col.gv()))
                else:
                    L.configure(text=col)


                if orientTop=="row":
                    if n==0:
                        L.configure( highlightbackground = Collor.fg, highlightthickness = 1)
                else:
                    if n2 == 0:
                        L.configure(anchor="w")
                    L.configure(highlightbackground=Collor.selector_none, highlightthickness=1)

                print(n2)
                L.grid(row=n,sticky="we",column=n2)
                print("i")
