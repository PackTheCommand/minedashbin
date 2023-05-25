import io
import os
import sys
import threading
import tkinter
from tkinter import *
from tkinter import ttk, font
from tkinter.ttk import Style, Sizegrip

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
        self.configure(undo=True)
        self.filetree=None
        self._orig = self._w + "_orig"
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.autocompletewindow = None
        self.kwws = []
        self.genMarkers()
        self.openFileName=None

        self.autocompVisible = True
        self.listbox: Listbox = None
        self.autocompleteOptions = []
        self.autocompleteVar = Variable(value=self.autocompleteOptions)

        self.bind("<Key>", lambda u: self.after(10, self.queryKww))

    def readJson(self):
        with open("editor_kww.json", encoding="UTF-8") as f:
            return json.loads(f.read())

    def genMarkers(self):
        self.colection = self.readJson()
        for k in self.colection[0]:
            self.kwws += self.colection[0][k]
        self.tag_configure("kww2", foreground="#B3679B")
        # strings #6A994E
        self.tag_configure("string", foreground="#6A994E")
        self.tag_configure("<>", foreground="#32A287")
        self.tag_configure("kww3", foreground="#FBB02D")
        self.tag_configure("kww4", foreground="#0E79B2")
        self.tag_configure("kww5", foreground="#F2C57C")
        self.tag_configure("comment", foreground="#746F72")

    def querylineForSpace(self, ind):
        ind1 = ind.split(".")[0]
        print("lst", self.index("end-1c linestart"))
        line = self.get(ind1 + ".0", ind1 + ".end")
        print("line", line)
        for n, l in enumerate(line[::-1]):
            if l == " ":
                print("found Space")
                return ind1 + f".{len(line) - n}"

        return ind1 + ".0"

    def bindAutoComplete(self):
        def selectUper(e):
            if self.autocompVisible:
                cur = self.listbox.curselection()
                if cur == ():
                    cur = (0,)
                print("fdsfds", cur)
                if cur[0] == 0:
                    return
                self.listbox.select_clear(cur[0])
                self.listbox.select_set(cur[0] - 1)

                return "break"

        def selectLower(e):
            print("kfjedwjo0ijoifgrejoijioüfdejiojhoiüferww")
            cur = self.listbox.curselection()
            if self.autocompVisible:
                if cur == ():
                    cur = (0,)
                print("fdsfds", cur)
                if cur[0] >= len(self.autocompleteOptions) - 1:
                    return
                self.listbox.select_clear(cur[0])
                self.listbox.select_set(cur[0] + 1)
                return "break"

        def complete(e):
            cur = self.listbox.curselection()
            if self.autocompVisible:
                if cur == ():
                    cur = (0,)
                ins = self.index(INSERT)
                spi = self.querylineForSpace(ins)
                print("spi", spi)
                self.replace(spi, ins, self.autocompleteOptions[cur[0]])
                self.hidePopup()

                return "break"

        self.bind("<Down>", selectLower)  #
        self.bind("<Escape>", lambda u: self.hidePopup())
        self.bind("<Tab>", complete)
        self.master.bind("<Configure>", lambda u: self.hidePopup())
        self.bind("<MouseWheel>", lambda u: self.hidePopup())
        self.bind("<FocusOut>", complete)
        self.bind("<Up>", selectUper)
        self.bind("<Control-s>", self.save)
    def save(self,u=None):
        fn=self.openFileName
        if fn==None:
            return
        with open(fn, "rb") as f:
            emstack=f.read()

        try:
            with open(fn, "w") as f:

                f.write( self.get("0.0",tkinter.END))
        except Exception:
            with open(fn, "wb") as f:
                f.write(emstack)



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

    def spawnPopup(self, index):
        b = self.bbox(index)
        # print(b,index)
        if b == None:
            return
        x, y = b[:2]
        x, y = x + self.winfo_rootx() - 40, y + self.winfo_rooty() + 20
        # print("e",b)

        if not self.autocompletewindow:
            self.autocompletewindow = w = Tk()
            w.configure(bg=Collor.bg_selected)
            listbox = Listbox(
                w, font=font.Font(family="Calibri", size=11, underline=False), borderwidth=0, highlightthickness=0,
                bg=Collor.bg_selected, fg=Collor.fg,
                selectbackground=Collor.selector_is,

                height=6,
                selectmode=tkinter.EXTENDED
            )
            listbox.pack(pady=(3, 3), padx=(5, 5))
            self.listbox = listbox
            w.overrideredirect(True)
            self.autocompVisible = True
            self.bindAutoComplete()
            w.geometry("+%s+%s" % (x, y))
        else:
            self.autocompletewindow.lift()
            self.listbox.delete(0, tkinter.END)
            for n, item in enumerate(self.autocompleteOptions):
                self.listbox.insert(n, item)
            self.listbox.update()
            if len(self.autocompleteOptions) <= 0:
                self.autocompVisible = False
                self.autocompletewindow.withdraw()
            else:
                self.autocompVisible = True
                self.autocompletewindow.deiconify()

            self.autocompletewindow.geometry("+%s+%s" % (x, y))

    def getPosible(self):
        ins = self.index(tkinter.INSERT)
        self.autocompleteOptions.clear()
        i2 = self.querylineForSpace(ins)
        value = self.get(i2, ins)
        if value.replace(" ", "") == "":
            return
        print("Value", value, ins, i2)

        for e in self.kwws:
            if e.startswith(value):
                self.autocompleteOptions.append(e)
            else:
                print(self.kwws)

        print(self.autocompleteOptions)
        if self.listbox:
            pass
            self.listbox.configure(height=len(self.autocompleteOptions))

    def queryKww(self):
        self.getPosible()
        self.autocompleteVar.set(self.autocompleteOptions)

        self.spawnPopup(self.index(tkinter.INSERT))

        for tag in self.colection[0].keys():
            self.tag_remove(tag, "0.0", self.index(tkinter.END))
        self.tag_remove("string", "0.0", self.index(tkinter.END))

        self.tag_remove("<>", "0.0", self.index(tkinter.END))

        for tag in self.colection[0].keys():
            for a in self.colection[0][tag]:
                st = "0.0"
                end = "0.0"
                stOld = ""
                while self.index(st) != self.index(tkinter.END):
                    st = self.search(a, end, tkinter.END)
                    if stOld == st:
                        break
                    stOld = st

                    print(st)
                    end = self.index('%s+%dc' % (st, len(a)))
                    alowedpars = ["[", "]" "(", ")", ".", " ", "\n"]
                    print("----", self.get('%s+%dc' % (end, 1)))
                    ec = self.get(self.index(end), self.index('%s+%dc' % (end, 1)))
                    bc = self.get(self.index('%s-%dc' % (st, 1)), self.index(st))
                    if (ec == "None") | (ec in alowedpars):
                        if (bc == "None") | (bc in alowedpars):
                            self.tag_add(tag, st, end)
                        else:
                            print("bc", bc, a, type(ec))
                    else:
                        print("ec", ec, a, type(ec))

        st = "0.0"
        end = "0.0"
        L = []
        L2 = []
        stOld = ""
        while self.index(st) != self.index(tkinter.END):
            st = self.search("\"", end, tkinter.END)
            if stOld == st:
                break
            stOld = st

            # print(st)
            end = self.index('%s+%dc' % (st, 1))
            L += [st]

        st = "0.0"
        end = "0.0"

        stOld = ""
        while self.index(st) != self.index(tkinter.END):
            st = self.search("<", end, tkinter.END)
            if stOld == st:
                break
            stOld = st

            # print(st)
            end = self.search(">", st, tkinter.END)
            L2 += [st, end]

        L3 = []
        st = "0.0"
        end = "0.0"
        while self.index(st) != self.index(tkinter.END):
            st = self.search("//", end, tkinter.END)
            if stOld == st:
                break
            stOld = st

            # print(st)
            end = self.search("\n", st, tkinter.END)
            L3 += [st, end]

        def placeMarkersFromList(list, tagname):

            while len(list) > 0:

                b = list.pop(0)
                try:
                    e = list.pop(0)
                except IndexError:

                    e = self.index(tkinter.END)
                    # print(e)

                for tag in self.colection[0].keys():
                    self.tag_remove(tag, b, self.index('%s+%dc' % (e, 1)))
                self.tag_add(tagname, b, self.index('%s+%dc' % (e, 1)))

        placeMarkersFromList(L2, "<>")
        placeMarkersFromList(L3, "comment")
        placeMarkersFromList(L, "string")

        # print("getString")

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
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.inwiget=False
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify="left",fg=Collor.fg,
                      background=Collor.bg_lighter, relief="solid", borderwidth=1,
                      font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
from graficsTk.notebook import TabBook

def CreateToolTip(widget1, text):
    toolTip = ToolTip(widget1)
    def enter(event):
        nonlocal widget1
        toolTip.inwiget=True
        def checkinw():
            if toolTip.inwiget:
                toolTip.showtip(text)
        widget1.after(1700,checkinw)
    def leave(event):
        toolTip.inwiget = False
        toolTip.hidetip()
    widget1.bind('<Enter>', enter)
    widget1.bind('<Leave>', leave)
import exeptions_
from contextlib import redirect_stdout
def openEditor(mainfile,dict1):
    t = Tk()
    t.title("Editor")
    t.geometry("%sx%s+10+10"%(t.winfo_screenwidth()-200,t.winfo_screenheight()-200))
    t.configure(bg=Collor.bg_lighter)
    a = FileTree(height=30, width=400)
    f = Frame(bg=Collor.bg_lighter)
    fb=Frame(bg=Collor.bg_lighter)
    s=Style()
    s.theme_use("clam")
    s.configure("special1.Horizontal.TProgressbar", foreground=Collor.Neutral, background=Collor.fg,troughcolor=Collor.bg,darkcolor=Collor.bg_lighter,lightcolor=Collor.bg_lighter,bordercolor=Collor.bg_lighter)
    p=ttk.Progressbar(
    fb,
    orient='horizontal',
    mode='determinate',
    length=280,style="special1.Horizontal.TProgressbar"
    )
    f.pack(fill="x")
    fb.pack(fill="x",side="bottom")
    fcon=Frame(bg=Collor.bg)
    fcon.pack(fill="x", side="bottom")
    tb=TabBook(master=fcon)
    tb.pack(fill="both",expand=True)
    consCount=0
    def createConsole(e,name=None):
        nonlocal consCount
        consCount+=1
        fr=Frame(bg=Collor.bg,master=tb)
        if name==None:
            name="Console "+str(consCount)
        f12 = TextBox(master=fr,font=font.Font(family="Calibre",size=14),height=11)
        r12 = tb.addTab(name, fr)
        f12.disable(True)

        f12.pack(fill="x")
        f12_imp = TextBox(master=fr, font=font.Font(family="Calibre", size=14), height=1)
        f12_imp.pack(fill="x")
        tb.nav(r12)

        def insertEnter(e):
            c=f12_imp.getValue()
            f12_imp.clear()
            f12.disable(False)
            f12.insert(tkinter.END,"\n>>> "+c)
            f12.disable(True)
            return "break"
        print("created")
        f12_imp.bind("<Return>",insertEnter)
        return f12,r12
    tb.addButton(text="➕",id=9999999,command=createConsole)

    """s=Sizegrip(master=fb)
    s.pack(side="right")"""
    lastbuildInfo=createLabel1(fb,"",bg=Collor.bg_lighter)
    lastbuildInfo.pack(side="right",anchor="se",padx=(0,20))




    b=LabelButton(master=f,img=createImage("imgs/compile_64.png",22,22))
    CreateToolTip(b,"Build Datapack")
    exeptions_.disableExit()
    strout=io.StringIO()
    con=None
    conid=None
    def compile():
        nonlocal strout,con,conid
        p.pack(side="right",padx=(0,20))

        p.start(8)
        text.save("")
        p.update()
        lastid=None
        last=False
        if con:
            lastid=conid
            last=True


        con,conid = createConsole("","Run")
        if last:
            tb.destroyTab(lastid)

        strout.close()
        strout=io.StringIO()

        def updateConsole(in_):
            try:
                insert = in_.getvalue()
            except ValueError:
                return

            strout.truncate(0)
            con.disable(False)
            con.insert(tkinter.END,insert)
            if insert!="":
                con.yview_pickplace("end")
            con.disable(True)
            t.after(50,lambda:updateConsole(in_))

        updateConsole(strout)


        try:
            with redirect_stdout(strout):

                ret=dict1["compile"]()
        except Exception:
            ret=False

        p.stop()
        p.pack_forget()
        if ret==False:
            lastbuildInfo.configure(fg=Collor.Error,text=" Build failed > "+exeptions_.exeptionreson)
            return

        lastbuildInfo.configure(fg=Collor.Success,text="Build finished after "+ret)
        lastbuildInfo.after(8000,lambda :lastbuildInfo.configure(text=""))
    def compThread():
        threading.Thread(target=compile).start()

    b.command(compThread)
    b.pack(side="right",anchor="e",padx=(0,26))


    print("path",mainfile[::-1].split("/",1)[1][::-1])
    a.generateFileTree(mainfile[::-1].split("/",1)[1][::-1].replace("/","\\"))

    def openfile(e=None,file=None):
        text.save()
        if not file:
            file = a.getFile()
        with open(file=file,mode="r", encoding='utf-8') as f:
            text.replace("0.0", tkinter.END, "")
            text.insert("0.0", f.read())
            text.queryKww()
        text.openFileName=file

    a.bind("<<OpenFile>>", openfile)


    a.pack(side="left",fill="both")
    fa = Frame(t,bg=Collor.bg)
    fa.pack(fill="both",expand=True)
    tel = LineNumberText_NumberBouard(fa, bg=Collor.bg_lighter, width=30,
                                      highlightbackground=Collor.bg)
    text = LineNumberText_Text(fa, insertbackground=Collor.fg, font=font.Font(size=13, family="Calibre"), bg=Collor.bg,
                               fg=Collor.fg)
    text.filetree=a
    openfile("",mainfile)

    text.pack(side="right",fill="both",expand=True)
    tel.pack(side="left", fill="y")
    text.bind("<<Change>>", tel.redraw)
    text.bind("<Configure>", tel.redraw)
    tel.attach(text)
    print(a.fileIds)
    t.mainloop()





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


def openSetup():
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

    i = TextBox(master=frame, height=1, width=20, font=f2)
    i.pack(anchor="center")

    # page 2

    frame2 = Frame(tk, width=400, height=280, name="null2", bg=Collor.bg)
    frame = frame2

    l = createLabel1(frame, "Select Your Source", font=f)
    l.pack()
    createLabel1(frame, "", font=f).pack()
    createLabel1(frame, "", font=f).pack()

    i2 = TextBox(master=frame, height=1, width=20, font=f2, state="disabled")
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

    i3 = TextBox(master=frame, height=1, width=20, font=f2, state="disabled")
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
        name, file, out = i.getValue().lower(), i2.getValue(), i3.getValue()
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
