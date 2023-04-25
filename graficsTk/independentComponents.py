import tkinter
import tkinter.font
from tkinter import Canvas, Tk, Frame, Label, Scale, Button, Text, END
from tkinter import ttk ,font as tkfont

import math
from tkinter.ttk import Separator


from PIL import Image, ImageTk,ImageColor,ImageGrab


from staticPy import Collor

"""
fr = Tk()
fr.title('Tkinter ColorPicker')
fr.configure(bg="#001414")
fr.geometry('300x300')
StatikImage = []

"""
StatikImage=[]

def createLabel1(master, text, textAncor="center", bg=Collor.bg, font=None,fs=12) -> Label:
    if font==None:
        font=tkfont.Font(size=fs, family="Bahnschrift")
    return Label(master, text=text, font=font, anchor=textAncor, bg=bg, fg=Collor.fg)

class Window(Tk):
    def __init__(self,**kwargs):
        self.updateable = {}
        Tk.__init__(self,**kwargs)
        self.win=Frame(master=self)
        self.win.place(x=0,y=0)
        self.notifications=[]
        self.defaultFont = tkfont.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Bahnschrift")

        self.wm_attributes('-transparentcolor',Collor.transparency_color)
        self.bind("<Configure>",self.__updateInerFrame)
        self.__updateInerFrame()
        style=ttk.Style()
        style.configure('TSeparator', foreground=Collor.fg)

    def __updateInerFrame(self,n=None):
        self.updateNotifications()
        self.win.configure(width=self.winfo_width(),height=self.winfo_height(),border=0)
    def updateNotifications(self):
        for a in self.updateable.keys():

            self.updateable[a].updateWinXY()
    def setBg(self,bg):
        self.win.configure(bg=bg)






class Notification(Frame):
    def __init__(self,title="Notification",width=60,height=None,**kwargs):
        Frame.__init__(self,bg=Collor.bg,width=width,height=height,**kwargs)
        """Note: Master Must determines position"""
        f=tkfont.Font(size=10,weight="bold")
        self.width=width
        self.height=height
        f2 = tkfont.Font( font="Calibri",size=4)
        fr=Frame(bg=Collor.bg,master=self)
        fr.pack(side="top",anchor="ne")
        self.w,self.h=width,height
        self.notifications:[*Notification]=[]
        fr2 = Frame(bg=Collor.bg, master=fr)
        fr2.pack(side="left", anchor="ne")

        L=Label(master=fr2,text=title,width=width-20,font=f2,bg=Collor.bg,fg=Collor.fg,anchor="w")
        L.pack(side="top",anchor="ne",fill="x")
        sep = Separator(master=fr2, orient='horizontal')

        sep.pack(side="bottom", anchor="n", fill="x")
        """L = Label(master=self, width=1,bg=Collor.bg)
        L.pack(side="bottom", anchor="n", fill="both",expand=True)
"""

        self.xbutton=BetterButton(master=fr,width=2,bg=Collor.bg,text="❌",fg=Collor.fg,font=f,anchor="e",command=self.hide)

        self.xbutton.pack(side="right",anchor="e")
    def hide(self):
        self.place_forget()
        print(self.master.updateable.keys())
        self.master.notifications.remove(self)
        self.master.updateable.pop(self)
        self.master.updateNotifications()

    def show(self):
        try:

            ofset = 0
            print(self.master.notifications)


            self.place(x=self.winfo_screenwidth(),y=0)
            self.master.notifications+=[self]


            self.master.updateable[self]=self

            self.updateWinXY()

        except ImportError:#Exception:
            raise Exception("Notification Object can only be used in containers using the pack window manager")
    def updateWinXY(self,u=None):
        def pl():
            x = self.master.winfo_width() - self.winfo_width()
            ofset=0
            for e in self.master.notifications:
                if e==self:
                    break
                if e.height==None:
                    ofset +=e.winfo_height()+2
                else:
                    ofset += e.height + 2
                #print(e.width)
            if self.h==None:
                self.h=self.winfo_height()
            y = self.master.winfo_height() - self.h - 10 - ofset
            self.place(x=x, y=y-20)

        self.after(100, pl)

def createImage(path, x, y,nsa=False):
    global StatikImage

    photo = Image.open(path)

    i = ImageTk.PhotoImage(photo.resize((x, y)), name=path)
    if not nsa:
        StatikImage += [i]
    return i

def createPhoto(path, x, y,nsa=False):
    global StatikImage

    photo = Image.open(path)
    #print(photo)
    StatikImage+=[photo]


    return photo
def photo_to_image(photo,x,y):
    global StatikImage
    #print(photo)
    i=ImageTk.PhotoImage(photo.resize((x, y)))
    StatikImage += [i]
    return i






class ModernColorPicker(Frame):
    def __init__(self,size=250,fg="black",**kw):
        """use Callback <<ColorSelected>> and in the function : ObjectName.getColor()"""
        super().__init__(**kw)

        self.size=s=size
        self.configure(width=s)
        bg=kw.get("bg")
        if not bg:
            bg="gray"
        self.oFrame=Frame(self,bg=bg)
        self.oFrame.pack(side="bottom")
        self.radius=self.size//2
        self.c= Canvas(master=self,width=s,height=s,borderwidth=0,highlightthickness=0,background=bg)
        self.selpos = None
        imagePath="resources/comp/color_weel.png"
        imagePath2 = "resources/comp/color_weel_suround.png"
        self.colorindicator=Label(master=self.oFrame,bg=bg,text="⬤",font=tkinter.font.Font(size=24))
        self.colorindicator.pack(side="left",anchor="ne")

        self.selectetcollor=[]

        self.otherImages=[]
        self.image = ImageTk.PhotoImage(Image.open(imagePath).resize((s,s)))
        self.image2=ImageTk.PhotoImage(Image.open(imagePath2).resize((s,s)))
        self.i2=self.c.create_image(0, 0, image=self.image2, anchor="nw")

        self.c.create_image(0,0,image=self.image,anchor="nw")
        self.opacityBLACK=self.create_rectangle(0,0,s,s,fill="#000000",alpha=0)

        self.c.bind("<Button-1>",self.setMarker)
        self.c.bind("<B1-Motion>", self.setMarker)
        self.c.pack()
        self.color="#000000"
        self.st=st = ttk.Style(self)

        self.coll_set=ttk.Button(self.oFrame,text="SET",width=4,command=lambda :self.event_generate("<<ColorSelected>>"))
        self.coll_set.pack(side="right")
        st.configure("Horizontal.TScale",background=bg)
        st.configure("TButton", background=bg,foreground=fg)
        st.map('TButton', background=[('active',bg)])


        self.sliderOpacity = ttk.Scale(self.oFrame, from_=-100, to=100,command=self.opacitisliderChange)
        self.sliderOpacity.pack(side="left",anchor="center",fill="x")

    def getColor(self):
        return self.color
    def opacitisliderChange(self,e):

        v=(self.sliderOpacity.get()//1)/100
        #print(v)
        if v<0:
            self.c.delete(self.opacityBLACK)
            self.otherImages.clear()


            self.opacity = self.create_rectangle(0, 0, self.size, self.size, fill="#000000", alpha=v*-1)
            self.c.lift(self.i2)
        else:
            self.c.delete(self.opacityBLACK)
            self.otherImages.clear()

            self.opacity = self.create_rectangle(0, 0, self.size, self.size, fill="#ffffff", alpha=v)
            self.c.lift(self.i2)
            pass



    def create_rectangle(self,x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.otherImages.append(ImageTk.PhotoImage(image))
            self.c.create_image(x1, y1, image=self.otherImages[-1], anchor='nw')
        self.c.create_rectangle(x1, y1, x2, y2, **kwargs)
    def rgb2hex(self,r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def get_color(self, x,y):
        x, y = self.c.winfo_rootx() + x, self.c.winfo_rooty() + y

        i = ImageGrab.grab((x, y, x + 1, y + 1))
        return i.getpixel((0, 0))
    def setMarker(self,e):


        x,y=e.x,e.y
        if self.point_in_circle(x,y,self.radius,self.radius,self.radius):
            if self.selpos!=None:
                self.c.delete( self.selpos)
            self.selpos=self.c.create_oval(x-5,y-5,x+5,y+5,width=2)

            #self.selectetcollor=s=#self.imgNpArray[x][y]
            rgb=self.get_color(x,y)
            self.color=self.rgb2hex(*rgb)
            self.colorindicator.configure(fg=self.color)





    def point_in_circle(self,x, y, x_center, y_center, radius):
        return math.sqrt((x - x_center) ** 2 + (y - y_center) ** 2) <= radius



class OptionButton(Frame):
    def __init__(self, name,width=None, chosen: int = None,bg=Collor.bg, chosenStr=None, options=[], onSelect=None,displayName:bool=False, **kw):
        super().__init__(bg=bg,**kw)
        self.names = options
        self.optItems = []
        self.onSelect = onSelect
        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        n = 0
        self.selected = -1
        if displayName:
            font2 = tkfont.Font(family="Bahnschrift", size=13, weight="bold")

            b = Label(master=self, text=name + " ", bg=Collor.bg, fg=Collor.fg, font=font2,anchor="nw")
            if width:
                b.configure(width=width)

            b.pack(side="top", anchor="nw",fill="x")
            self.configure(highlightthickness=1,highlightbackground=Collor.highlight)


        fr=Frame(master=self,bg=Collor.bg)
        fr.pack(side="top",fill="both",padx=(10,10),pady=(3,2))

        for o in options:

            b = Label(master=fr, text=o, bg=Collor.selector_none, fg=Collor.fg,
                       font=font_size_medium, bd=0,highlightbackground=Collor.fg)

            b.bind("<Button-1>", lambda u, num=n: self.setSelected(n=num))

            b.pack(side="left", anchor="ne",padx=(2,2))

            self.optItems += [b]

            n += 1
        if chosen != None:
            self.setSelected(chosen)

        if chosenStr != None:
            self.setSelectedStr(chosenStr)

    def setSelected(self, n):
        if self.onSelect:
            self.onSelect(n)
        self.selected = n
        for nu, item in enumerate(self.optItems):

            if (nu == n):
                item.configure(bg=Collor.selector_is, fg=Collor.fg,highlightthickness=1)
                continue
            item.configure(bg=Collor.selector_none, fg=Collor.fg,highlightthickness=0
                           )
        return n
        pass

    def setSelectedStr(self, str):

        for n, s in enumerate(self.names):
            b = self.optItems[n]

            if (s == str):
                self.selected = n
                b.configure(bg=Collor.selector_is, fg=Collor.fg,highlightthickness=1)
                continue
            b.configure(bg=Collor.selector_none, fg=Collor.fg,highlightthickness=0)

        pass

    def getSelectedId(self):
        return self.selected

    def getSelectedItem(self):
        # print(self.selected)
        if self.selected == -1:
            return None

        return self.names[self.selected]


class Animation():
    def __init__(self,master,time=100,flow="fluid",type="move",repeat="infinite",colorflow_from_to=["#000000","#ffffff"]):
        """
        type: should be "move" or "color-flow" or
        flow: should be "fluid" or "stepped"
        repeat: should be integer or "infinite"
        time: int  in ms
        colorflow_from_to: aray with the two colors if type is color-flow > format is "#color-in-hex"

        """
        self.master=master
        self.time = time
        if type=="color-flow":
            self.color_flow_dict=self.rgbBlend(colorflow_from_to[0],colorflow_from_to[1])
            self.colorflow_from_to=colorflow_from_to

        self.flow = flow
        self.type = type
        self.repeat =repeat

    def start(self,element):
        """
        element: the tkinter object that the animation should be run on

        """

        if self.type=="color-flow":
            def cl_flow_repeat_limited(e,repeat_circle,ftime,ret=[True]):

                frame_time=ftime

                if ret[0]:
                    ret[0]=False
                    ret =self.transform_color(len(self.color_flow_dict), -1, element, ftime=ftime, ret=ret)

                    repeat_circle -= 1

                if (repeat_circle > 0):
                    self.master.after(frame_time,lambda e=e,rp=repeat_circle:cl_flow_repeat_limited(e,rp,ftime,ret=ret))

            def cl_flow_repeat_infinite(e,ftime,ret=[True]):


                if ret[0]:
                    ret =self.transform_color(len(self.color_flow_dict), -1, element, ftime=ftime)


                self.master.after(self.time, lambda e=e: cl_flow_repeat_infinite(e,ftime,ret=ret))


            ftime=self.time//len(self.color_flow_dict)
            if (self.repeat == "infinite"):
                cl_flow_repeat_infinite(element,ftime)
            else:
                cl_flow_repeat_limited(element,self.repeat,ftime)
        if self.type=="move":
            pass






    def color_flow(self):
        pass

    def rgbBlend(self, h1, h2):
        r1, g1, b1 = ImageColor.getrgb(h1)
        r2, g2, b2 = ImageColor.getrgb(h2)


        l1 = [r1, g1, b1]
        l2 = [r2, g2, b2]
        addl = []
        rl = []
        for i in range(0, len(l1)):
            a, b = l1[i], l2[i]
            addl += [(a - b) / 20]

        def rgbh(r):
            s = '%02x' % int(r)
            if len(s) < 3:
                s = "0" + s
            return s

        for i in range(0, 20):
            rl += [
                f"#{rgbh(l1[0] + addl[0] * i)}{rgbh(l1[1] + addl[1] * i)}{rgbh(l1[2] + addl[2] * i)}".replace("-",
                                                                                                              "")]


        return rl
    def transform_color(self, n, add=1, item=None, ftime=20, ret=[False]):

        n+=add
        item.configure(bg=self.color_flow_dict[n])
        if not(n<=0):

            self.master.after(ftime, lambda:self.transform_color(n, add, item, ret=ret))
        else:
            ret[0]=True

        return ret





class ImageTransformButton(Frame):
    def __init__(self, chosen: int = None, options:list[str,str]=["",""],colors=["#000000","#ffffff"],optionSize=(50,40) ,onSelect=None, **kw):
        super().__init__(**kw)
        self.names = options
        self.colors=colors
        self.inTransform=False
        self.onSelect = onSelect
        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        n = 0
        self.optionSize=optionSize
        self.selected = -1
        self.images=[]
        self.transforming=self.rgbBlend(colors[0],colors[1])
        # print(f"{n=}")
        path=options[1]
        i=createImage(path,optionSize[0],optionSize[1])


        b = Label(master=self, image=i, bg=Collor.bg,
                      highlightbackground=Collor.bg_darker, font=font_size_medium, highlightthickness=2, bd=0)

        b.bind("<Button-1>", lambda u, num=n: self.setSelected(n=num))

        b.pack(side="left", anchor="ne")

        self.optItem =b

        n += 1
        if chosen != None:
            self.setSelected(chosen)

    def transform(self,n,add=1):

        n+=add
        self.optItem.configure(bg=self.transforming[n])
        if (n!=19)&(not(n<=0)):

            self.after(20,lambda:self.transform(n,add))
        else:
            self.inTransform = False
        if (n==10):
            self.optItem.configure(image=createImage(self.names[self.selected], self.optionSize[0], self.optionSize[1]))

    def setSelected(self, n):
        if(self.inTransform):
            return
        self.inTransform=True
        if self.onSelect:
            self.onSelect(n)
        if self.selected==0:
            self.selected=1
        else:

            self.selected=0

        if self.selected==0:
            print(10101010)
            self.transform(0, 1)
            return

        self.transform(19, -1)
    def rgbBlend(self,h1,h2):
        r1,g1,b1=ImageColor.getrgb(h1)
        r2,g2,b2=ImageColor.getrgb(h2)


        l1=[r1,g1,b1]
        l2=[r2,g2,b2]
        addl=[]
        rl=[]
        for i in range(0,len(l1)):
            a,b=l1[i],l2[i]
            addl+=[(a-b)/20]

        def rgbh(r):
            s ='%02x' % int(r)
            if len(s)<3:
                s="0"+s
            return s


        for i in range(0,20):


            rl += [f"#{rgbh(l1[0] + addl[0] * i)}{rgbh(l1[1] + addl[1] * i)}{rgbh(l1[2]+addl[2]*i)}".replace("-","")]


        return rl



    def getSelectedId(self):
        return self.selected

    def getSelectedItem(self):
        # print(self.selected)
        if self.selected == -1:
            return None

        return self.names[self.selected]


class BetterButton(Button):
    def __init__(self, bg=Collor.bg, fg=Collor.fg,font=None, **kn):
        if font==None:
            font=tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        super().__init__(bg=bg, fg=fg, highlightthickness=1, bd=0, font=font,
                         **kn)

class PopUpMenuScreen(Frame):
    def __init__(self,titel,width=100,height=10,**kwargs):
        Frame.__init__(self,width=width,height=height,bg=Collor.bg,**kwargs)
        fontTitel = tkfont.Font(family="Bahnschrift", size=14, weight="bold")
        Label(self,bg=Collor.bg,fg=Collor.fg,font=fontTitel,text=titel,width=24,highlightthickness=0).pack(side="top",fill="x")


class MovableFrame(Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.placeing = []
        self.lastOrder = 0

    def move(self, mx=0, my=0, order=0):
        if self.placeing == []:
            self.placeing = [int(self.place_info()["x"]), int(self.place_info()["y"])]
        x, y = self.placeing[0], self.placeing[1]
        nx, ny = x + mx, y + my
        self.placeing = [nx, ny]
        self.place_configure(x=nx, y=ny)


class LabelButton(Label):
    def __init__(self, img, command=None, args=(), **kw):

        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        super().__init__(image=img, bg=Collor.bg_darker, highlightthickness=1,
                         highlightbackground=Collor.fg_inverted, font=font_size_medium, **kw)

        self.commandf = command
        self.i = img
        self.args = args

        self.bind("<Button-1>", self.klickListener)
        def f(u):
            self.configure(bg=Collor.bg, highlightbackground=Collor.fg_inverted)
            if self.commandf:
                self.commandf(*self.args)

        self.bind("<ButtonRelease-1>", f)
    def command(self,command):
        self.commandf=command

    def klickListener(self, u):
        global tagsActive

        self.configure(bg=Collor.bg_selected, highlightbackground=Collor.fg)

class StickyButton(Label):
    def __init__(self, img, command=None, args=(), **kw):

        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        super().__init__(image=img, bg=Collor.bg_darker, highlightthickness=1,
                         highlightbackground=Collor.fg_inverted, font=font_size_medium, **kw)

        self.commandf = command
        self.i = img
        self.args = args
        self.state = False
        self.bind("<ButtonRelease-1>", self.klickListener)



    def command(self,command):
        self.commandf=command
    def forceState(self,state:bool):
        self.klickListener("",forceState=state,nocom=True)
    def klickListener(self, u,forceState=None,nocom=False):

        global tagsActive
        if not forceState:
            self.state=not self.state
        else:
            self.state=forceState
        if self.state:
            if self.commandf:
                if not nocom:

                    self.commandf("active",*self.args)
            self.configure(bg=Collor.bg_selected, highlightbackground=Collor.fg)

        else:
            if self.commandf==None:
                if not nocom:

                    self.commandf("inactive",*self.args)

            self.configure(bg=Collor.bg, highlightbackground=Collor.fg_inverted)



class ScroledTextBox(Text):
    def __init__(self, NumRange=(0, 10),lapOver=True, **kw):
        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        super().__init__(bg=Collor.bg_darker, height=1, fg=Collor.fg, font=font_size_medium,
                         highlightthickness=0, highlightbackground="black", highlightcolor="black", **kw)
        self.bind("<Return>", self.e)
        self.bind("<Key>", self.br)
        self.bind("<MouseWheel>", self.scroll)
        #self.event_add("<<ValueChange>>",None)
        self.list = [i for i in range(NumRange[0], NumRange[1] + 1)]
        self.ind = 0
        self.lapOver=lapOver
        self.setValue(self.list[0])
        self.curs=Frame()

    def scroll(self, e):




        if e.delta > 1:

            if  (not self.lapOver)&(self.ind>=len(self.list)-1):

                return
            self.ind += 1
            if (self.ind > len(self.list) - 1):
                self.ind = 0
        else:

            if  (not self.lapOver)&(self.ind<=0):
                return
            self.ind -= 1
            if (self.ind <= -1):
                self.ind = len(self.list) - 1

        self.setValue(self.list[self.ind])


    def e(self, u):
        return "break"

    def br(self, u):
        return "break"

    def setValue(self, text):
        self.clear()

        self.insert("0.0", text)
        self.event_generate("<<ValueChange>>")

    def getValue(self):
        return self.get("0.0", END).replace("\n", "")

    def clear(self):
        self.replace("0.0", END, "")


class TextBox(Text):
    def __init__(self, max_lines, width2=0, start=None, disable_height_change=True, **kw):
        font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
        super().__init__(bg=Collor.bg_darker, fg=Collor.fg, font=font_size_medium, **kw)
        self.bind("<Return>", self.e)
        self.widthNum = width2
        self.max_lines = max_lines

        """if not disable_height_change:

            self.bind("<Key>", lambda u: self.after(10, self.updateHeight))"""

        if start:
            self.insert("0.0", start)
        if not disable_height_change:
            self.updateHeight()

    def e(self, u):
        return "break"

    def setValue(self, text):
        self.clear()
        self.insert("0.0", text)

    def updateHeight(self):
        le = len(self.getValue())
        h = 1 + (le // self.widthNum) // 2
        if h > self.max_lines:
            h = self.max_lines
        self.configure(height=h)
        # print(h)

        self.winfo_width()

    def insertWhileDisabled(self, value):
        self.disable(False)
        self.addValueAtEnd(value)
        self.disable(True)

    def getValue(self):
        return self.get("0.0", END).replace("\n", "")

    def clear(self):
        self.replace("0.0", END, "")

    def disable(self, b: bool):
        if b:
            self["state"] = "disabled"
        else:
            self["state"] = "normal"

    def addValueAtEnd(self, value):
        self.insert(tkinter.END, value)
class ScrollableFrame(Frame):
    def __init__(self,width=100,height=100,bg=Collor.bg,**kw):


        super().__init__(bg=bg,width=width,height=height,**kw)

        f = Frame(master=self, bg=bg)
        self.innerFrame=f
        self.width=width
        self.height=height
        f.place(x=0, y=0,width=width,height=height)
        self.re_bind()
        #f.bind("<MouseWheel>", lambda e: self.onScroll(e, f))
        f.bind()
        ef=Frame(master=self,width=width*10,height=4,bg=Collor.selector_none)
        ef.place(x=0,y=height-4)
        ef.bind("<Configure>",self.updateHeight)

        self.curs=Frame(master=self,bg=Collor.highlight,height=10,width=6,highlightthickness=0)
        Label(master=self.curs)
        self.curs.place(y=0,x=-6,height=10,)

    def updateHeight(self,u):
        #print("h",self.innerFrame.winfo_height(),self.innerFrame.place_info())
        self.innerFrame.place_configure(height=self.innerFrame.winfo_reqheight())
    def forget_bind(self):
        self.unbind_all("<MouseWheel>")
    def re_bind(self):
        self.innerFrame.bind_class('.', "<MouseWheel>",lambda e: self.onScroll(e))
        self.innerFrame.configure(highlightbackground=Collor.selector_none,highlightcolor=Collor.selector_none)

    def updateWidth(self,u):
        self.configure(width=self.innerFrame.winfo_width())
        self.innerFrame.bind_class('.', "<MouseWheel>", lambda e: self.onScroll(e))
    def onScroll(self,e):
        self.updateHeight(1)
        print(e)
        f=self.innerFrame
        y = int(f.place_info()["y"])
        w = int(f.winfo_reqheight()) - self.winfo_height()
        # print(self)

        if e.delta > 0:
            y += 20
        else:
            y -= 20
        print(y+self.winfo_height(),self.innerFrame.winfo_reqheight())
        if ((-y) > w):
            print("None")
            return
        elif ((y) > 0):
            print("None")
            return

        f.place_configure(y=y)
        if y==0:
            y=1
        hight_frame=self.winfo_height()
        rest=hight_frame/self.innerFrame.winfo_height()
        #print(hight_frame, self.innerFrame.winfo_height(), (y),rest,self.width,hight_frame/rest)

        new_height = hight_frame*rest

        #print(new_height, self.height)
        self.curs.configure(height =new_height,)

        self.curs.place_configure(y=((hight_frame*rest)-new_height)-y,height=new_height,x=self.winfo_width()-6)



    def getInnerFrame(self):
        return self.innerFrame