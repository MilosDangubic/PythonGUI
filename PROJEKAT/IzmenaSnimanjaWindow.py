from  tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from snimanja import *
from pacijent import  *

class IzmenaSnimanjaWindow(Tk):
    def __init__(self,snimanjaWindow,snimanje):
        super().__init__()
        self.__pacijenti=Pacijent.loadPacijenti()
        self.__snimanjaWindow=snimanjaWindow
        self.__snimci=self.__snimanjaWindow.snimci
        self.__snimanje=snimanje
        self.addComponents()

    def addComponents(self):
        title = "IzmenaSnimanja snimanja"
        self.title(title)
        self._cyan3="cyan3"
        window = Frame(self,background= self._cyan3)
        window.pack(side=LEFT, fill=BOTH, expand=1)

        self.__PacijentCombo=Combobox(window)
        self.__tipCombo=Combobox(window)
        self.__tipCombo['values']=('MRI','CT scan','X-ray','Ultrasonography')

        self.__textID = StringVar(self)
        self.__IDEntry = Entry(window, state=NORMAL, textvariable=self.__textID)
        self.__textVreme=StringVar(self)
        self.__VremeEntry=Entry(window, state=NORMAL, textvariable=self.__textVreme)
        self.__textDatum = StringVar(self)
        self.__datumEntry = Entry(window, state=NORMAL, textvariable=self.__textDatum)
        self.__textIzvestaj = StringVar(self)
        self.__izvestajEntry = Entry(window,state=NORMAL, textvariable=self.__textIzvestaj)
        self.__textLekar = StringVar(self)
        self.__lekarEntry = Entry(window, state=NORMAL, textvariable=self.__textLekar)
        self.__textDicom = StringVar(self)
        self.__dicomEntry = Entry(window, state='readonly', textvariable=self.__textDicom)

        self._cyan2='cyan2'
        Label(window, text="ID: ",bg=self._cyan2).grid(row=0, column=0, sticky=E)
        self.__IDEntry.grid(row=0, column=1, sticky=E)
        Label(window, text="Pacijent: ",bg=self._cyan2).grid(row=1, column=0, sticky=E)
        self.__PacijentCombo.grid(row=1, column=1)

        Label(window, text="Datum: ",bg=self._cyan2).grid(row=2, column=0, sticky=E)
        self.__datumEntry.grid(row=2, column=1, sticky=E)
        Label(window,text="Vreme: ",bg=self._cyan2).grid(row=3,column=0,sticky=E)
        self.__VremeEntry.grid(row=3,column=1,sticky=E)

        Label(window, text="Tip: ",bg=self._cyan2).grid(row=4, column=0, sticky=E)
        self.__tipCombo.grid(row=4, column=1, sticky=E)
        Label(window, text="Izvestaj: ",bg=self._cyan2).grid(row=5, column=0, sticky=E)
        self.__izvestajEntry.grid(row=5, column=1, sticky=E)
        Label(window, text="Lekar: ",bg=self._cyan2).grid(row=6, column=0, sticky=E)
        self.__lekarEntry.grid(row=6, column=1, sticky=E)
        Label(window, text="Dicom: ",bg=self._cyan2).grid(row=7, column=0, sticky=E)
        self.__dicomEntry.grid(row=7,column=1,sticky=E)

        self.__sacuvajButton = Button(window, text='Sacuvaj snimanje', command=self.sacuvajSnimanje, state=NORMAL)
        self.__sacuvajButton.grid(row=0, column=2)
        self.__odustaniButton = Button(window, text='Odustani', command=self.odustani, state=NORMAL)
        self.__odustaniButton.grid(row=1,column=2)

        for key in self.__pacijenti.keys():
            if self.__pacijenti[key].lbo not in self.__PacijentCombo['values']:
                imePrezime=self.__pacijenti[key].ime+" "+self.__pacijenti[key].prezime
                self.__PacijentCombo['values'] = (*self.__PacijentCombo['values'], imePrezime)

        self.popuniPolja()


    def sacuvajSnimanje(self):

        self.__snimanje.lekar = self.__textLekar.get()
        dat = self.datumValidacija()
        if not dat:
            return
        dat=self.datumValidacija()
        if not dat:
            return

        vr=self.VremeValidacija()
        if not vr:
            return
        self.__snimanje.vreme=vr
        self.__snimanje.datum = dat
        self.__snimanje.tip = self.__tipCombo.get()
        self.__snimanje.izvestaj = self.__textIzvestaj.get()
        self.__snimanje.dicom = self.__textDicom.get()
        self.__snimci[self.__snimanje.id] = self.__snimanje
        self.__snimanjaWindow.popuniListBox(self.__snimci)
        self.__snimanjaWindow.lift()
        self.__snimanjaWindow.isprazniEntry()
        self.destroy()
    def searchByLbo(self, lbo):
        for keys in self.__pacijenti.keys():
            if self.__pacijenti[keys].lbo == lbo:
                return self.__pacijenti[keys]
    def popuniPolja(self):
        self.__textID.set(self.__snimanje.id)
        self.__textDatum.set(self.__snimanje.datum)
        self.__textDicom.set(self.__snimanje.dicom)
        self.__textLekar.set(self.__snimanje.lekar)
        self.__textVreme.set(self.__snimanje.vreme)
        self.__textIzvestaj.set(self.__snimanje.izvestaj)
        self.__tipCombo.set(self.__snimanje.tip)
        pacijent=self.searchByLbo(self.__snimanje.pacijent)
        imePrezime=pacijent.ime+" "+pacijent.prezime
        self.__PacijentCombo.set(imePrezime)
    def odustani(self):
        self.__snimanjaWindow.lift()
        self.destroy()

    def datumValidacija(self):
        datum = datetime.now()
        datumString = self.__textDatum.get()
        d = self.__textDatum.get()
        datumString = datumString.split(".")
        if len(datumString) != 3:
            messagebox.showerror("Greska", "Datum nije validan1")
            return None
        dan = int(datumString[0])
        mesec = int(datumString[1])
        godina = int(datumString[2])
        if godina < datum.year:
            messagebox.showerror("Greska", "Datum nije validan")
            return None
        elif godina == datum.year:
            if mesec < datum.month:
                messagebox.showerror("Greska", "Datum nije validan")
                return None
            elif mesec == datum.month:
                if dan < datum.day:
                    messagebox.showerror("Greska", "Datum nije validan")
                    return None
                else:
                    return d

            else:
                return d
        else:
            return d

    def VremeValidacija(self):
        vremeStr = self.__textVreme.get()
        lista = vremeStr.split(":")
        if len(lista) != 2:
            messagebox.showerror("Greska", "Vreme nije validno")
            return None
        sati = int(lista[0])
        minuti = int(lista[1])
        if sati < 0 or sati >= 24:
            messagebox.showerror("Greska", "Vreme nije validan")
            return None
        if minuti < 0 or minuti >= 60:
            messagebox.showerror("Greska", "Vreme nije validan")
            return None
        return vremeStr
