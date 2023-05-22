import os
import tkinter
from datetime import datetime
from time import strftime, gmtime
from tkinter import Canvas, Tk,font,Frame
from .staticPy import Collor
from .independentComponents import  *
class Chat(Canvas):
    def __init__(self,**kwargs):
        super(Chat, self).__init__(bg=Collor.bg,**kwargs)
        self.lowest_level =100
        self.moveble=[]
        self.scrollLevel=0
        self.x_end=0
        self.current_smothscroll=0
        self.msg_font= font.Font(size=12,family="Bahnschrift")
        self.sender_font = font.Font(size=10, family="Bahnschrift")
        self.date_font = font.Font(size=8, family="Bahnschrift")
        self.bind("<MouseWheel>",self.smoothscroll)
        self.after(2000,self.scrollToLowestLevel)
    def addtolevel(self,x):
        self.lowest_level+=x
        self.x_end+=x
    def scroll(self,e):
        print(e)
        scroll=int(e.delta/10)
        self.move("all", 0,scroll)


    def smoothscroll(self,e):
        print(e)
        self.current_smothscroll+=1
        if self.current_smothscroll==99999:
            self.current_smothscroll=0
        scroll = -int(e.delta)
        def doscroll(n,id):
            n=int(n)
            if self.current_smothscroll!=id:
                return
            if -4<n<4:
                return
            re=n/3

            if (re<0)&(self.lowest_level>self.x_end):

                return
            if (re > 0) & (self.lowest_level - self.winfo_height() <0):

                return

            self.move("all", 0, -re)
            self.lowest_level -= re
            self.after(40,lambda :doscroll(n-re,id))

        doscroll(scroll,self.current_smothscroll)
    def scrollToLowestLevel(self):
        while True:
            if (self.lowest_level - self.winfo_height() < 0):
                break
            self.lowest_level-=20
            self.move("all", 0, -20)
    def getLongest(self,str1):
        ml=0
        its=""
        for i in str1:
            if len(i)>ml:
                its=i

        return its
    def post(self,message,sender,senderIsSelf=True,customColor=None,notriangle=False):


        #tr1-text
        text=self.create_text(22, self.lowest_level + 14, text=message, fill=Collor.Polar, font=self.msg_font, anchor="nw")

        box=self.bbox(text)
        self.update()
        width=box[2]-box[0]+10
        height=box[3]-box[1]+5
        xOfset=0
        #tr2-text
        text2 = self.create_text(22, self.lowest_level + 14, text=sender+"12fd2", fill=Collor.Polar, font=self.msg_font,
                                anchor="nw")
        box2 = self.bbox(text2)
        self.update()
        width2 = box2[2] - box2[0] + 10
        print(width2,width,".",box2,box)
        if width2>width:
            width=width2
        #done
        if senderIsSelf:
            xOfset = self.winfo_width() - (width + 40)
        self.delete(text)
        self.delete(text2)
        text = self.create_text(xOfset+ 22, self.lowest_level + 14, text=message, fill=Collor.Polar, font=self.msg_font,
                                anchor="nw")


        sendtext=self.create_text(xOfset+20, self.lowest_level, text=sender, fill=Collor.Polar, anchor="nw", font=self.sender_font)
        self.update()
        userNamebox = self.bbox(text)

        ofsetDatewidth = userNamebox[2] - userNamebox[0] +4
        min_width = width + 22 + ofsetDatewidth
        bubleX1,bubleX2=xOfset+10,xOfset+20+width


        if customColor:
            rectColor =customColor

        else:
            rectColor=Collor.ChatBuble
        r=self.create_round_rectangle(bubleX1,self.lowest_level,bubleX2,self.lowest_level+height+10,fill=rectColor)
        self.lift(sendtext)
        self.update()
        bb = self.bbox(r)
        self.lift(text)
        print(ofsetDatewidth)
        if senderIsSelf:
            tr1X, tr1Y = xOfset+width-40, self.lowest_level + height + 10
            if not notriangle: tri=self.create_triangle(tr1X, tr1Y, tr1X + 15, tr1Y, tr1X+30, tr1Y + 15, fill=Collor.ChatBuble)

            timetext = self.create_text( self.winfo_width()-70, self.lowest_level + 4,
                                        text=strftime("%H:%M:%S", gmtime()), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)

        else:
            timetext = self.create_text(bb[2]-50 , self.lowest_level + 2,
                                        text=strftime("%H:%M:%S", gmtime()), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)
            tr1X, tr1Y=40,self.lowest_level+height+10
            if not notriangle: tri=self.create_triangle(tr1X,tr1Y,tr1X+15,tr1Y,tr1X-5,tr1Y+20 ,        fill=Collor.ChatBuble)

        if not notriangle:
            tr = self.bbox(tri)
            height = (bb[3] - bb[1])+(tr[3] - tr[1] + 20)
        else:
            height = (bb[3] - bb[1]) + 20


        self.addtolevel(height)

        if not notriangle:
            self.moveble+=[r,sendtext,text,tri,timetext]
        else:
            self.moveble += [r, sendtext, text, timetext]
        self.scrollToLowestLevel()

    def postImage(self,sender,imgName,senderIsSelf=False,size=180,cornerradius=None):
        # tr1-text
        imgpath=getPath()+"\\emotes\\"+imgName+".png"
        if senderIsSelf:
            mesage_image = self.create_image(self.winfo_width()-size-33, self.lowest_level+10 ,image=createImage(imgpath,size,size,cornerRadius=cornerradius),
                                    anchor="nw",)
        else:
            mesage_image = self.create_image(23, self.lowest_level + 10,
                                     image=createImage(imgpath, size, size, cornerRadius=cornerradius),
                                     anchor="nw", )

        box = self.bbox(mesage_image)
        self.update()
        width = box[2] - box[0] + 10
        xOfset = 0

        text2 = self.create_text(22, self.lowest_level + 14, text=sender + "12fd2", fill=Collor.Polar,
                                 font=self.msg_font,
                                 anchor="nw")
        box2 = self.bbox(text2)
        self.update()
        width2 = box2[2] - box2[0] + 10
        print(width2, width, ".", box2, box)
        if width2 > width:
            width = width2

        if senderIsSelf:
            xOfset = self.winfo_width() - (width + 40)

        self.delete(text2)
        self.lift(mesage_image)

        sendtext = self.create_text(xOfset + 20, self.lowest_level-8, text=sender, fill=Collor.Polar, anchor="nw",
                        font=self.sender_font)
        userNamebox = self.bbox(mesage_image)
        self.update()
        ofsetDatewidth = userNamebox[2] - userNamebox[0] + 4
        self.lift(mesage_image)
        if senderIsSelf:
            timetext = self.create_text(self.winfo_width() - 70, self.lowest_level-10 + 4,
                                        text=strftime("%H:%M:%S", gmtime()), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)
        else:
            timetext = self.create_text(xOfset + 20 + ofsetDatewidth - 40, self.lowest_level-10 + 4,
                                        text=strftime("%H:%M:%S", gmtime()), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)
        bb=box
        height = (bb[3] - bb[1]) + 20+ (box2[3] - box2[1])

        self.addtolevel(height-10)

        self.moveble += [ sendtext, mesage_image,timetext]
        self.scrollToLowestLevel()
    def postImageWithBuble(self,sender,imgName,senderIsSelf=False,size=180,cornerradius=None):
        # tr1-text
        imgpath=getPath()+"\\emotes\\"+imgName+".png"
        text = self.create_image(self.winfo_width()-size-33, self.lowest_level+10 ,image=createImage(imgpath,size,size,cornerRadius=cornerradius),
                                anchor="nw",)

        box = self.bbox(text)
        self.update()
        width = box[2] - box[0] + 10
        height = (box[3] - box[1] + 5)+12
        xOfset = 0
        # tr2-text
        text2 = self.create_text(22, self.lowest_level + 14, text=sender + "12fd2", fill=Collor.Polar,
                                 font=self.msg_font,
                                 anchor="nw")
        box2 = self.bbox(text2)
        self.update()
        width2 = box2[2] - box2[0] + 10
        print(width2, width, ".", box2, box)
        if width2 > width:
            width = width2
        # done
        if senderIsSelf:
            xOfset = self.winfo_width() - (width + 40)

        self.delete(text2)
        self.lift(text)

        sendtext = self.create_text(xOfset + 20, self.lowest_level-8, text=sender, fill=Collor.Polar, anchor="nw",
                                    font=self.sender_font)
        userNamebox = self.bbox(text)
        self.update()
        ofsetDatewidth = userNamebox[2] - userNamebox[0] + 4
        min_width = width + 22 + ofsetDatewidth
        bubleX1, bubleX2 = xOfset + 10, xOfset + 20 + width

        r = self.create_round_rectangle(bubleX1, self.lowest_level-10, bubleX2, self.lowest_level + height + 10,
                                        fill=Collor.ChatBuble)
        self.lift(sendtext)

        self.lift(text)
        if senderIsSelf:
            tr1X, tr1Y = xOfset + width - 40, self.lowest_level + height + 10
            #tri = self.create_triangle(tr1X, tr1Y, tr1X + 15, tr1Y, tr1X + 30, tr1Y + 15, fill=Collor.ChatBuble)

            timetext = self.create_text(self.winfo_width() - 70, self.lowest_level-10 + 4,
                                        text=datetime.now().strftime("%H:%M:%S"), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)

        else:
            print("ofsetDatewidth",ofsetDatewidth)
            timetext = self.create_text(xOfset + 20 + ofsetDatewidth - 40, self.lowest_level-10 + 4,
                                        text=datetime.now().strftime("%H:%M:%S"), fill=Collor.Polar, anchor="nw",
                                        font=self.date_font)
        bb = self.bbox(r)

        height = (bb[3] - bb[1]) + 20

        self.addtolevel(height-10)

        self.moveble += [r, sendtext, text]
        self.scrollToLowestLevel()
    def create_round_rectangle(self,x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,x1 + radius, y1,x2 - radius, y1,x2 - radius, y1,
                  x2, y1,x2, y1 + radius,x2, y1 + radius,x2, y2 - radius,
                  x2, y2 - radius,x2, y2,x2 - radius, y2,x2 - radius, y2,x1 + radius, y2,
                  x1 + radius, y2,x1, y2,x1, y2 - radius,x1, y2 - radius,x1, y1 + radius,
                  x1, y1 + radius,x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)
    def create_triangle(self,x1, y1, x2, y2,x3,y3, **kwargs):
        points = [x1, y1, x2, y2,x3,y3]

        return self.create_polygon(points, **kwargs)
def warpWord(m,max_length):
    lastWarp=-1
    finalMessage=""
    count=0
    for char in m:
        if char==" ":
            lastWarp=len(finalMessage)
        if count==max_length:
            print("added \\n")
            finalMessage=finalMessage[:lastWarp]+"\n"+finalMessage[lastWarp:]
            count=0
            lastWarp=-1
        count+=1
        finalMessage+=char
    return finalMessage.replace("\n ","\n")
class roundetText(Frame):
    def __init__(self,text_width=40,sendcommand=None,openEmoComand=None,**kwargs):

        super(roundetText, self).__init__(bg=Collor.bg,**kwargs)
        #self.create_round_rectangle(0, 0, 300,44 ,fill="red")

        f=tkinter.font.Font(size=12,family="Bahnschrift")
        tf=Frame(master=self,bg=Collor.bg)
        tf.pack(side="left")

        e=Text(master=tf,font=f,wrap="word",height=2,bg=Collor.bg,width=text_width,highlightthickness=1,highlightbackground=Collor.ChatBuble,insertbackground=Collor.fg,fg=Collor.fg)

        e.pack(padx=(5,2),pady=(4,4),fill="x",)

        """st = ttk.Style(e)
        st.theme_use("clam")

        st.configure("TEntry", background=Collor.bg, foreground=Collor.bg, tabmargins=0, borderwidth=0, margin=20, padding=[5, 1],
                        highlightbackground="red", bordercolor=Collor.bg,
                        )
        st.map("chatSendEntry.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],
                      'border':''
                               '0', 'sticky': 'nswe'})])
        st.configure("chatSendEntry.TEntry",
                         background=Collor.ChatBuble,
                         foreground=Collor.fg,
                            highlightbackground="red",
                         fieldbackground=Collor.bg)

        #self.create_window(10,10,window=e,anchor="nw")
        e.configure(style="chatSendEntry.TEntry")"""
        im=createImage(getPath()+"\\imgs\\send_message_64.png",22,22,name="messageSentImage")

        im2 = createImage(getPath() + "\\imgs\\done.png", 22, 22, name="messageSentImage")

        def send_():
            text = e.get("0.0", tkinter.END)
            e.replace("0.0", tkinter.END, "")
            if text.endswith("\n"):
                sendcommand(text[:-1])
                return
            sendcommand(text)
        def doubleRetsent(u=None):
            e.after(10, send_)
            return "break"
        def br(u=None):
            return "break"
        e.bind("<Double-Return>", doubleRetsent)
        e.bind("<Double-Enter>", doubleRetsent)
        e.bind("<Return>", br)
        e.bind("<Enter>", br)

        b2 = ttk.Button(master=self, text="", style="TButton", width=20, image=im2, command=openEmoComand)

        b=ttk.Button(master=self,text="",style="TButton",width=20,image=im,command=send_)
        aplyttkStyler(b)

        b.pack(side="right",padx=(2,2),pady=(2,2),)
        b2.pack(side="right", padx=(0, 2), pady=(2, 2), )

def getImagesInDir(dir,resolution,cornerrad=None):
    fileImgs={}
    for i in os.listdir(getPath()+"\\"+dir):
        if i.find(".") == -1:
            continue
        ext, type = i.split(".", 1)
        #ext = ext.replace("_64", "")
        if type == "png":
            im = createImage(getPath()+"\\"+dir+"\\" + i, resolution,resolution, name="img3x73s_" + ext,cornerRadius=cornerrad)
            fileImgs[ext] = im

    return fileImgs

def getPath():
    f = str(__file__)
    fs = f[::-1].split("\\", 1)[1]
    return fs[::-1]
import game.modernApi as API
class ChatFrame(tkinter.Frame):
    def __init__(self,master,width=200,height=300,name="Unknown",username="Unknown",api=None,hidecommand=None,**kwargs):
        super(ChatFrame, self).__init__(width=width,height=height,master=master,**kwargs)
        fr=Frame(self, bg=Collor.bg)
        #fr.pack(side="top",fill="x")
        self.fr=fr
        self.lastheigt=None
        self.hidecommand=hidecommand
        self.width=width
        l=Label(master=fr,bg=Collor.bg,image=createImage("gresource/done_64.png",32,32,name="img_chat_ico"))
        l.pack(side="left")
        l = Label(master=fr, bg=Collor.bg ,fg=Collor.fg,text=name,font=("Bahnschrift-14"))
        l.pack(side="left",fill="x",padx=(5,2))
        def hide():
            self.pack_forget()
            if self.hidecommand!=None:
                self.hidecommand()
        l=LabelButton(master=fr,img=createImage("gresource/cancel_64.png",22,22),command=lambda:self.hide(hide))
        l.pack(side="right")
        self.EmoFrame=None
        self.update()
        self.api=api
        self.username=username
        self.ch = Chat(master=self,width=width, height=height)
        self.ch.pack(fill="y")
        self.after(0,lambda:self.ch.post("You entered The Chat","System",False,customColor=Collor.Success,notriangle=True))
        self.after(100,self.ch.scrollToLowestLevel)




        self.update()
    def openEmojiWin(self):
        if self.lastheigt!=None:
            self.ch.configure(height=self.lastheigt-4)
            self.input.configure(height=self.inputFrameHeight)
            self.ch.pack_configure(fill="y")
            if self.EmoFrame:
                self.EmoFrame.pack_forget()
            self.lastheigt=None
            print("hide")

            return
        self.lastheigt=self.ch.winfo_height()
        self.inputFrameHeight=self.input.winfo_height()

        self.ch.configure(height=self.lastheigt-150)

        print("show")
        if self.EmoFrame==None:
            def sendImage(iamge):
                self.ch.postImage(self.username,imgName=iamge,senderIsSelf=True,cornerradius=20)
                self.openEmojiWin()
            self.EmoFrame=Frame(master=self,height=160,width=self.width)
            sf=ScrollableFrame(master=self.EmoFrame,width=self.width,height=160,highlightbackground=Collor.fg,highlightthickness=3)
            sf.pack()

            sf=sf.innerFrame

            x=0
            y=0
            imgs=getImagesInDir("emotes",60,cornerrad=50)
            for i in imgs.keys():
                if x==4:
                    x=0
                    y+=1

                LabelButton(master=sf,img=imgs[i],command=sendImage,args=(i,)).grid(column=x,row=y)
                x+=1




        self.EmoFrame.pack(after=self.ch)

    def show(self):


        self.pack(side="right", fill="y", )
        slightHightToMaxPack(self,self.width,at_end=lambda:self.fr.pack(side="top",fill="x",before=self.ch))

    def setlineBreaks(self,m):

        n=10
        splitted_str= [m[i:i + n] for i in range(0, len(m), n)]
        result: str = "\n".join(splitted_str)
        return result

    def trigerMessageSendEvent(self,m):
        self.api.EventHandler.trigger("msgChatSend",m)
        pass
    def createInput(self,width=40):
        def send(text):

            if text.replace(" ","").replace("\n","")=="":
                return

            w=warpWord(text,20)
            print(w)
            self.ch.post(w,"You",True)
            self.trigerMessageSendEvent({"sender":self.username,"message":w,"type":"text"})

        self.input=roundetText(master=self,height=100,sendcommand=send,text_width=width,openEmoComand=self.openEmojiWin)
        self.input.pack(fill="x",side="bottom")
    def hide(self,atEnd):
        print("dkawspokpfsd")
        self.fr.pack_forget()

        slightHightToNull(self,atEnd)

if __name__ == "__main":
    tk=Tk()

    c=ChatFrame(username="RAscal")
    c.pack()
    c.createInput()
    tk.mainloop()


