import os
from tkinter import *
from tkinter import ttk
from graficsTk import *
import tkinter.filedialog as fd









exit()


def getPathFile(i, ft, fileOfset=""):
    path = fd.askopenfile(
        title='SelectOutput',
        initialdir="C:\\",
        filetypes=[*ft])
    if path:
        i.setValue(path.name)
def getPathDir(i, stateafter="normal"):
    path = fd.askdirectory(
        title='SelectOutput',
        initialdir="C:\\",)
    if path:
        i.setValue(path)










def open():
    tk=Window()
    tk.wm_geometry("400x340")
    tk.resizable(True,False)
    tk.configure(bg=Collor.bg)
    N=ModernNotebook(master=tk,disableTabSelection=True)
    N.pack(fill="both")
    frameButNextLast = Frame(tk, bg=Collor.bg)
    frameButNextLast.pack(side="bottom", pady=(1, 5))
    bnext = BetterButton(text="Next >", bg=Collor.selector_is, command=N.forward)
    bnext.pack(side="right", padx=(0, 5))
    bback = BetterButton(text="< Back", bg=Collor.selector_is, command=N.backward)
    bback.pack(side="left", padx=(5, 0))
    #Page1
     # .Tab
    frame1 = Frame(tk, width=400, height=280,name="null1",bg=Collor.bg)
    frame=frame1
    f= tkfont.Font(size=22,family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l=createLabel1(frame,"Give your Project a name",font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i=TextBox(master=frame, height=1,width=20,font=f2,insertbackground=Collor.fg)
    i.pack(anchor="center")

    #page 2

    frame2 = Frame(tk, width=400, height=280,name="null2",bg=Collor.bg)
    frame=frame2

    l = createLabel1(frame, "Select Your Source", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i2 = TextBox(master=frame, height=1, width=20,  font=f2, insertbackground=Collor.fg,state="disabled")
    i2.pack(anchor="center")
    B=BetterButton(master=frame,text="Select Source",borderwidth=1,command=lambda:getPathFile(i2,(("mcdb","*.mcdb"),("all","*.*"))))
    B.pack()



    #page 3
    frame3 = Frame(tk, width=400, height=280, name="null3", bg=Collor.bg)
    frame = frame3
    f = tkfont.Font(size=22, family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l = createLabel1(frame, "Select Output Dir", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i3 = TextBox(master=frame, height=1, width=20, font=f2, insertbackground=Collor.fg,state="disabled")
    i3.pack(anchor="center")
    B = BetterButton(master=frame, text="Select Output", borderwidth=1, command=lambda: getPathDir(i3,))
    B.pack()

    frame4 = Frame(tk, width=400, height=280, name="null4", bg=Collor.bg)
    frame = frame4
    f = tkfont.Font(size=22, family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l = createLabel1(frame, "Finish And Create Project", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()
    r=[]
    def create():
        nonlocal i,i2,i3,r,tk
        i.configure(bg=Collor.bg),i2.configure(bg=Collor.bg),i3.configure(bg=Collor.bg)
        if ((i.getValue()=="")):
            N.nav(0)
            i.configure(bg=Collor.Error)


            return
        name,file,out=i.getValue().lower(), i2.getValue().lower(), i3.getValue().lower()
        if not (os.path.exists(file)):
            N.nav(1)
            i2.configure(bg=Collor.Error)

            return
        if not (os.path.exists(out)):
            N.nav(2)
            i3.configure(bg=Collor.Error)
            return


        r=[i.getValue().lower(),i2.getValue().lower(),i3.getValue().lower()]
        tk.destroy()

    B = BetterButton(master=frame, text="Create", borderwidth=1, command=create)



    B.pack()

    N.addframe(frame1)

    N.addframe(frame2)

    N.addframe(frame3)
    N.addframe(frame4)









    tk.mainloop()
    return r
