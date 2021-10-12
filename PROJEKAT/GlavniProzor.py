from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pacijent import *
from snimanja import *
from  datetime import datetime
from PIL import Image as Img
from PIL import ImageTk


import  SnimanjaWindow
from PacijentWindow import *
class GlavniProzor(Tk):
    def __init__(self):
        super().__init__()
        self.addComponents()

    def addComponents(self):
        self.title("Snimanja za radiografiju")
        #fotografija
        imgPath = "logo.png"
        loadImg = Img.open(imgPath)
        w, h = loadImg.size
        canv = Canvas(self, bg="blue", width=w, height=h)
        render = ImageTk.PhotoImage(loadImg)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0, relwidth=1, relheight=1)
        canv.pack()

        filemenu=Menu(self)
        datotekaMeni = Menu(filemenu, tearoff = 0)
        datotekaMeni.add_command(label = "Izlaz", command = self.Izadji)
        filemenu.add_cascade(label = "Opcija za izlaz", menu = datotekaMeni)

        opcijeMeni = Menu(filemenu, tearoff=0)
        opcijeMeni.add_command(label="Pacijenti", command=self.otvoriPacijente)
        opcijeMeni.add_command(label="Snimci", command=self.otvoriSnimke)
        filemenu.add_cascade(label="Pacijenti i snimanja", menu=opcijeMeni)


        self.config(menu=filemenu)
        # Izlaz iz aplikacije klikom na X
        self.protocol("WM_DELETE_WINDOW", self.Izadji)




    def otvoriPacijente(self):
        p=PacijentWindow()
        p.mainloop()


    def otvoriSnimke(self):
        snimci=SnimanjaWindow.SnimanjaWindow()
        snimci.mainloop()

    def Izadji(self):
        odgovor = messagebox.askokcancel("Snimanja za radiografiju", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()



