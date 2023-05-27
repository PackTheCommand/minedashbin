from tkinter import Canvas, Tk, Frame
import minedashbin.graficsTk as gtk
from minedashbin.graficsTk import Collor

root=Tk()


class PathShow(Frame):
    def __init__(self):
        super().__init__(self)
        self.labels=[]
    def cl(self,name):
        l=gtk.createLabel1(self,name,bg=Collor.bg)
        l.pack(side="left")

        self.labels+=[l]
        def enter():

            l.configure(bg=Collor.bg_lighter)


        def leave():

            l.configure(bg=Collor.bg)


        l.bind("<Enter>", lambda u: enter())
        l.bind("<Leave>", lambda u: leave())

    def adddecorator(self, symbol):
        l = gtk.createLabel1(self, symbol, bg=Collor.bg)
        l.pack(side="left")

        self.labels += [l]
    def delall(self):
        for e in self.labels:
            e.destroy()


root.mainloop()