from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pacijent import *
from snimanja import *
from  datetime import datetime

import  SnimanjaWindow
import DodajPacijentaWindow

class IzmenaWindow(Tk):

    def __init__(self, lbo,pacijentiWindow):
        super().__init__()
        self.__lbo = lbo
        self.__pacijentiWindow=pacijentiWindow
        self.__pacijenti =self.__pacijentiWindow.pacijenti
        self.__pacijent = self.__pacijenti[lbo]
        self.addComponents()
        self.popuniEntryPolja(self.__pacijent)

    def addComponents(self):
        self.title("Izmena")
        window = Frame(self, padx=5, pady=5, borderwidth=2)
        window.pack(side=RIGHT)

        self.__textLBO = StringVar(self)
        self.__LBOEntry = Entry(window,state = 'readonly', textvariable = self.__textLBO)
        self.__textIme = StringVar(self)
        self.__imeEntry = Entry(window,state = NORMAL,textvariable = self.__textIme)
        self.__textPrezime = StringVar(self)
        self.__prezimeEntry = Entry(window,state = NORMAL,textvariable = self.__textPrezime)
        self.__textDatum = StringVar(self)
        self.__DatumEntry = Entry(window,state = NORMAL,textvariable = self.__textDatum)

        Label(window,text="Ime: ").grid(row=0,column=0,sticky=E)
        self.__imeEntry.grid(row=0,column=1,sticky=W)
        Label(window,text="Prezime: ").grid(row=1,column=0,sticky=E)
        self.__prezimeEntry.grid(row=1,column=1,sticky=W)
        Label(window,text="LBO: ").grid(row=2,column=0,sticky=E)
        self.__LBOEntry.grid(row=2,column=1,sticky=W)
        Label(window,text="Datum rođenja:").grid(row=3,column=0,sticky=E)
        self.__DatumEntry.grid(row=3,column=1,sticky=W)

        self.__btnSacuvajIzmenu = Button(window,text = 'Sačuvaj izmenu', command = self.sacuvajIzmene, state = NORMAL)
        self.__btnSacuvajIzmenu.grid(row = 4, column  = 1, sticky = E)

        self.__btnNazad = Button(window, text="Nazad", command=self.nazad, state=NORMAL)
        self.__btnNazad.grid(row=5, column=1, sticky=E)

    def popuniEntryPolja(self, pacijent):
        self.__textLBO.set(pacijent.lbo)
        self.__textIme.set(pacijent.ime)
        self.__textPrezime.set(pacijent.prezime)
        self.__textDatum.set(pacijent.datum)

    def sacuvajIzmene(self):
        ime=self.imeValidacija()
        if not ime:
            return
        prezime=self.prezimeValidacija()
        if not prezime:
            return


        datum=self.datumValidacija()
        if not datum:
            return

        if messagebox.askquestion("Upozorenje", "Da li ste sigurni da želite da sačuvate izmene?", icon="warning") == "yes":
            self.__pacijent.ime = ime
            self.__pacijent.prezime = prezime
            self.__pacijent.datum = datum
            self.__pacijenti[self.__lbo]=self.__pacijent
            self.__pacijentiWindow.fillListBox(self.__pacijenti)
            Pacijent.savePacijenti(self.__pacijenti)
            self.destroy()
            self.__pacijentiWindow.obrisiEntryPolja()
            self.__pacijentiWindow.lift()



    def imeValidacija(self):
        ime = self.__textIme.get()
        if len(ime) < 2:
            messagebox.showerror("Greška", "Ime pacijenta mora sadržati bar 2 karaktera!")
            self.lift()
            return None
        return ime

    def prezimeValidacija(self):
        prezime = self.__textPrezime.get()
        if len(prezime) < 2:
            messagebox.showerror("Greška", "Prezime mora sadržati bar 2 karaktera")
            return None
        return prezime

    def datumValidacija(self):
        datum = datetime.now()
        d=self.__textDatum.get()
        datumString = self.__textDatum.get()
        datumString = datumString.split(".")

        dan = int(datumString[0])
        mesec = int(datumString[1])
        godina = int(datumString[2])

        if godina > datum.year:
            messagebox.showerror("Greška", "Datum nije validan!")
            return None
        elif godina == datum.year:
            if mesec > datum.month:
                messagebox.showerror("Greška", "Datum nije validan!")
                return None
            elif mesec == datum.month:
                if dan > datum.day:
                    messagebox.showerror("Greška", "Datum nije validan!")
                    return None
                else:
                    return d

            else:
                return d
        else:
            return d

    def ocisti(self):
        self.__textLBO.set("")
        self.__textIme.set("")
        self.__textPrezime.set("")
        self.__textDatum.set("")

    def nazad(self):
        self.destroy()
