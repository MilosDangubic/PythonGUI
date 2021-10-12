from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pacijent import *
from snimanja import *
from  datetime import datetime

import  SnimanjaWindow
import PacijentWindow

class DodajPacijentaWindow(Tk):

    def __init__(self,pacijentWindow):
        super().__init__()
        self.__pacijentWindow=pacijentWindow
        self.addComponents()

    def addComponents(self):
        self.title("Dodaj pacijenta")
        window = Frame(self, padx=5, pady=5, borderwidth=2)
        window.pack(side=LEFT)

        self.__textLBO = StringVar(self)
        self.__LBOEntry = Entry(window, state=NORMAL, textvariable=self.__textLBO)
        self.__textIme = StringVar(self)
        self.__imeEntry = Entry(window, state=NORMAL, textvariable=self.__textIme)
        self.__textPrezime = StringVar(self)
        self.__prezimeEntry = Entry(window, state=NORMAL, textvariable=self.__textPrezime)
        self.__textDatum = StringVar(self)
        self.__DatumEntry = Entry(window, state=NORMAL, textvariable=self.__textDatum)
        self.__textSearch = StringVar(self)
        self.__searchEntry = Entry(window, state=NORMAL, textvariable=self.__textSearch)

        Label(window, text="Ime: ").grid(row=0, column=0, sticky=E)
        self.__imeEntry.grid(row=0, column=1, sticky=W)
        Label(window, text="Prezime: ").grid(row=1, column=0, sticky=E)
        self.__prezimeEntry.grid(row=1, column=1, sticky=W)
        Label(window, text="LBO: ").grid(row=2, column=0, sticky=E)
        self.__LBOEntry.grid(row=2, column=1, sticky=W)
        Label(window, text="Datum rođenja:").grid(row=3, column=0, sticky=E)
        self.__DatumEntry.grid(row=3, column=1, sticky=W)

        self.__btnSacuvajPacijenta = Button(window, text='Sačuvaj', command=self.sacuvajPacijenta, state=NORMAL)
        self.__btnSacuvajPacijenta.grid(row=5, column=3, sticky=E)

        self.__btnNazad = Button(window, text = "Nazad", command=self.nazad, state = NORMAL)
        self.__btnNazad.grid(row=6, column=3, sticky=E)

    def sacuvajPacijenta(self):
        lbo = self.LBOValidacija()
        if not lbo:
            return
        ime = self.imeValidacija()
        if not ime:
            return
        prezime = self.prezimeValidacija()
        if not prezime:
            return
        datum = self.datumValidacija()
        if not datum:
            return

        if messagebox.askquestion("Upozorenje", "Da li ste sigurni da želite da sačuvate pacijenta?", icon="warning") == "yes":

            pacijent = Pacijent(lbo, ime, prezime, datum)
            self.__pacijentWindow.pacijenti[lbo]=pacijent
            Pacijent.savePacijenti(self.__pacijentWindow.pacijenti)
            self.__pacijentWindow.fillListBox(self.__pacijentWindow.pacijenti)
            self.destroy()
            self.__pacijentWindow.lift()
    def LBOValidacija(self):
        pacijenti = self.__pacijentWindow.pacijenti
        lbo = self.__textLBO.get()
        if len(lbo) != 11:
            messagebox.showerror("Greška", "LBO  mora imati 11 cifara!")
            return None
        else:
            for keys in sorted(pacijenti):
                if pacijenti[keys].lbo==lbo:
                    messagebox.showerror("Greška","Već postoji uneti LBO!")
                    return None
            return lbo

    def imeValidacija(self):
        ime = self.__textIme.get()
        if len(ime) < 2:
            messagebox.showerror("Greška", "Ime pacijenta mora sadržati bar 2 karaktera!")
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





    def nazad(self):
        self.destroy()
