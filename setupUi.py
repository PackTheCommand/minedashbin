import os
import tkinter
from tkinter import *
from tkinter import ttk, font

import _tkinter
from pyrr.rectangle import height

from graficsTk import *
import tkinter.filedialog as fd

from minedashbin.graficsTk.fileEditor import FileTree


class LineNumberText_NumberBouard(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textComp = None
    def attach(self, text_widget):
        self.textComp = text_widget
    def redraw(self, *args):
        self.delete("all")
        i = self.textComp.index("@0,0")
        while True:
            _dline = self.textComp.dlineinfo(i)
            if _dline == None:
                break
            y = _dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="white",
                             font=font.Font(family="Bahnschrift", size=12, weight="bold"))
            i = self.textComp.index("%s+1line" % i)
class LineNumberText_Text(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.autocompletewindow=None
        self.genMarkers()
        self.kwws=["func","controller","functio"]
        self.autocompVisible=True
        self.listbox:Listbox = None
        self.autocompleteOptions=[]
        self.autocompleteVar=Variable(value=self.autocompleteOptions)

        self.bind("<Key>", lambda u: self.after(10, self.queryKww))

    def genMarkers(self):
        self.colection = [{"kww": ["if", "else","shr ",""],"kww2": ["include", "native",],"kww3": ["(", ")",";","[","]",],"kww4": ["func",]}]
        self.tag_configure("kww", foreground=Collor.Warn)
        self.tag_configure("kww2", foreground="#B3679B")
        # strings #6A994E
        self.tag_configure("string", foreground="#6A994E")
        self.tag_configure("kww3", foreground="#FBB02D")
        self.tag_configure("kww4", foreground="#0E79B2")

    def querylineForSpace(self,ind):
        ind1 = ind.split(".")[0]
        print("lst",self.index("end-1c linestart"))
        line=self.get(ind1+".0",ind1+".end")
        print("line",line)
        for n,l in enumerate(line[::-1]):
            if l==" ":
                print("found Space")
                return ind1+f".{len(line)-n}"

        return ind1+".0"


    def bindAutoComplete(self):
        def selectUper(e):
            if self.autocompVisible:
                cur=self.listbox.curselection()
                if cur ==():
                    cur=(0,)
                print("fdsfds",cur)
                if cur[0]==0:
                    return
                self.listbox.select_clear(cur[0])
                self.listbox.select_set(cur[0]-1)


                return "break"
        def selectLower(e):
            print("kfjedwjo0ijoifgrejoijioüfdejiojhoiüferww")
            cur = self.listbox.curselection()
            if self.autocompVisible:
                if cur ==():
                    cur=(0,)
                print("fdsfds", cur)
                if cur[0]>=len(self.autocompleteOptions)-1:
                    return
                self.listbox.select_clear(cur[0])
                self.listbox.select_set(cur[0]+1)
                return "break"
        def complete(e):
            cur = self.listbox.curselection()
            if self.autocompVisible:
                if cur == ():
                    cur = (0,)
                ins=self.index(INSERT)
                spi=self.querylineForSpace(ins)
                print("spi",spi)
                self.replace(spi,ins,self.autocompleteOptions[cur[0]])
                self.hidePopup()


                return "break"

        self.bind("<Down>",selectLower)#
        self.bind("<Escape>",lambda u:self.hidePopup())
        self.bind("<Tab>",complete)
        self.bind("<Up>",selectUper)
    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
        except _tkinter.TclError:
            return
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        return result
    def hidePopup(self):
        self.autocompVisible = False
        self.autocompletewindow.withdraw()
    def spawnPopup(self,index):
        b=self.bbox(index)
        # print(b,index)
        if b==None:
            return
        x,y=b[:2]
        x,y=x+self.winfo_rootx()-40,y+self.winfo_rooty()+20
        #print("e",b)

        if not self.autocompletewindow:
            self.autocompletewindow=w=Tk()
            w.configure(bg=Collor.bg_selected)
            listbox = Listbox(
                w,font=font.Font(family="Calibri",size=11,underline=False),borderwidth=0,highlightthickness=0,bg=Collor.bg_selected,fg=Collor.fg,
                selectbackground=Collor.selector_is,

                height=6,
                selectmode=tkinter.EXTENDED
            )
            listbox.pack(pady=(3,3),padx=(5,5))
            self.listbox=listbox
            w.overrideredirect(True)
            self.autocompVisible = True
            self.bindAutoComplete()
            w.geometry("%s+%s"%(x,y))
        else:
            self.autocompletewindow.lift()
            self.listbox.delete(0,tkinter.END)
            for n,item in enumerate(self.autocompleteOptions):
                self.listbox.insert(n,item)
            self.listbox.update()
            if len(self.autocompleteOptions)<=0:
                self.autocompVisible=False
                self.autocompletewindow.withdraw()
            else:
                self.autocompVisible = True
                self.autocompletewindow.deiconify()

            self.autocompletewindow.geometry("+%s+%s" % (x, y))

    def getPosible(self):
        ins=self.index(tkinter.INSERT)
        self.autocompleteOptions.clear()
        i2=self.querylineForSpace(ins)
        value=self.get(i2,ins)
        if value.replace(" ","")=="":
            return
        print("Value",value,ins,i2)

        for e in self.kwws:
            if e.startswith(value):
                self.autocompleteOptions.append(e)
            else:
                print(self.kwws)


        print(self.autocompleteOptions)


    def queryKww(self):
        self.getPosible()
        self.autocompleteVar.set(self.autocompleteOptions)

        self.spawnPopup(self.index(tkinter.INSERT))

        for tag in self.colection[0].keys():
            self.tag_remove(tag,"0.0",self.index(tkinter.END))
        self.tag_remove("string", "0.0", self.index(tkinter.END))

        for tag in self.colection[0].keys():
            for a in self.colection[0][tag]:
                st="0.0"
                end="0.0"
                stOld=""
                while self.index(st)!=self.index(tkinter.END):
                    st = self.search(a, end, tkinter.END)
                    if stOld==st:


                        break
                    stOld = st

                    print(st)
                    end = self.index('%s+%dc' % (st, len(a)))

                    self.tag_add(tag, st, end)

        st = "0.0"
        end = "0.0"
        L=[]
        stOld = ""
        while self.index(st) != self.index(tkinter.END):
            st = self.search("\"", end, tkinter.END)
            if stOld == st:
                break
            stOld = st

            #print(st)
            end = self.index('%s+%dc' % (st, 1))
            L+=[st]



        while len(L)>0:

            b=L.pop(0)
            try:
                e=L.pop(0)
            except IndexError:

                e=self.index(tkinter.END)
                #print(e)

            for tag in self.colection[0].keys():
                self.tag_remove(tag,b,self.index('%s+%dc' % (e,1)))
            self.tag_add("string",b,self.index('%s+%dc' % (e,1)))

        #print("getString")

    def getStringSeperated(string, splitonspace=True):
        retStr = [""]

        enter = False
        disabled = False
        for char in string:
            if splitonspace & (char == " ") & (not enter):
                retStr[-1] += char
                retStr += [""]
                continue

            if ((char == "\"") | (char == "'")) & (not disabled):

                enter = not enter
                if enter:
                    retStr += [""]
                else:
                    retStr[-1] += char
                    retStr += [""]
                    continue
            if disabled:
                disabled = False
            if (char == "\"") & enter:
                disabled = True
            if enter:
                add = True

            retStr[-1] += char
        return retStr



def openEditor():
    t = Tk()
    a = FileTree(height=30, width=400)
    f = Frame(bg=Collor.bg_lighter)
    f.pack()
    a.generateFileTree(r"C:\Users\ctind\PycharmProjects\PYDatabase\minedashbin\\minedashbin")

    def openfile(e):
        file = a.getFile()
        with open(file,encoding='utf-8') as f:

            text.replace("0.0", tkinter.END, "")
            text.insert("0.0", f.read())
            text.queryKww()

    a.bind("<<OpenFile>>", openfile)

    a.pack(side="left")
    tel = LineNumberText_NumberBouard(t, bg=Collor.bg_lighter, width=30,
                                      highlightbackground=Collor.bg)
    text = LineNumberText_Text(t, insertbackground=Collor.fg, font=font.Font(size=13, family="Calibre"), bg=Collor.bg,
                               fg=Collor.fg)
    text.pack(side="right", fill="y", expand=True)
    tel.pack(side="right", fill="y", expand=True)
    text.bind("<<Change>>", tel.redraw)
    text.bind("<Configure>", tel.redraw)
    tel.attach(text)
    print(a.fileIds)
    t.mainloop()


openEditor()
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
        initialdir="C:\\", )
    if path:
        i.setValue(path)


def open():
    tk = Window()
    tk.wm_geometry("400x340")
    tk.resizable(True, False)
    tk.configure(bg=Collor.bg)
    N = ModernNotebook(master=tk, disableTabSelection=True)
    N.pack(fill="both")
    frameButNextLast = Frame(tk, bg=Collor.bg)
    frameButNextLast.pack(side="bottom", pady=(1, 5))
    bnext = BetterButton(text="Next >", bg=Collor.selector_is, command=N.forward)
    bnext.pack(side="right", padx=(0, 5))
    bback = BetterButton(text="< Back", bg=Collor.selector_is, command=N.backward)
    bback.pack(side="left", padx=(5, 0))
    # Page1
    # .Tab
    frame1 = Frame(tk, width=400, height=280, name="null1", bg=Collor.bg)
    frame = frame1
    f = tkfont.Font(size=22, family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l = createLabel1(frame, "Give your Project a name", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i = TextBox(master=frame, height=1, width=20, font=f2, insertbackground=Collor.fg)
    i.pack(anchor="center")

    # page 2

    frame2 = Frame(tk, width=400, height=280, name="null2", bg=Collor.bg)
    frame = frame2

    l = createLabel1(frame, "Select Your Source", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i2 = TextBox(master=frame, height=1, width=20, font=f2, insertbackground=Collor.fg, state="disabled")
    i2.pack(anchor="center")
    B = BetterButton(master=frame, text="Select Source", borderwidth=1,
                     command=lambda: getPathFile(i2, (("mcdb", "*.mcdb"), ("all", "*.*"))))
    B.pack()

    # page 3
    frame3 = Frame(tk, width=400, height=280, name="null3", bg=Collor.bg)
    frame = frame3
    f = tkfont.Font(size=22, family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l = createLabel1(frame, "Select Output Dir", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i3 = TextBox(master=frame, height=1, width=20, font=f2, insertbackground=Collor.fg, state="disabled")
    i3.pack(anchor="center")
    B = BetterButton(master=frame, text="Select Output", borderwidth=1, command=lambda: getPathDir(i3, ))
    B.pack()

    frame4 = Frame(tk, width=400, height=280, name="null4", bg=Collor.bg)
    frame = frame4
    f = tkfont.Font(size=22, family="Bahnschrift")
    f2 = tkfont.Font(size=18, family="Bahnschrift")
    l = createLabel1(frame, "Finish And Create Project", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()
    r = []

    def create():
        nonlocal i, i2, i3, r, tk
        i.configure(bg=Collor.bg), i2.configure(bg=Collor.bg), i3.configure(bg=Collor.bg)
        if ((i.getValue() == "")):
            N.nav(0)
            i.configure(bg=Collor.Error)

            return
        name, file, out = i.getValue().lower(), i2.getValue().lower(), i3.getValue().lower()
        if not (os.path.exists(file)):
            N.nav(1)
            i2.configure(bg=Collor.Error)

            return
        if not (os.path.exists(out)):
            N.nav(2)
            i3.configure(bg=Collor.Error)
            return

        r = [i.getValue().lower(), i2.getValue().lower(), i3.getValue().lower()]
        tk.destroy()

    B = BetterButton(master=frame, text="Create", borderwidth=1, command=create)

    B.pack()

    N.addframe(frame1)

    N.addframe(frame2)

    N.addframe(frame3)
    N.addframe(frame4)

    tk.mainloop()
    return r
