from  tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from DicomWindow import DicomWindow
from snimanja import *
from pacijent import  *
from DodajSnimanjeWindow import  *
from  IzmenaSnimanjaWindow import  *
class SnimanjaWindow(Tk):
    def __init__(self):
        super().__init__()
        self.__snimci=Snimak.loadSnimci()
        self.__pacijenti=Pacijent.loadPacijenti()
        self.addComponents()
        self.popuniListBox(self.__snimci)

    def addComponents(self):
        self.__snimciListBox = Listbox(self,width=40)
        self.__snimciListBox.pack(side=RIGHT)
        title = "Snimci"
        self.title(title)
        self.__snimciListBox.bind("<<ListboxSelect>>", self.promenaSelekcije)
        self._cyan3='cyan3'
        window = Frame(self,background= self._cyan3)
        window.pack(side=LEFT, fill=BOTH, expand=1)

        self.__PacijentCombo=Combobox(window)
        self.__tipCombo=Combobox(window)
        self.__tipCombo['values']=('MRI','CT scan','X-ray','Ultrasonography')
        self.__tipCombo.bind("<<ComboboxSelected>>", self.ComboChange)
        self.__PacijentCombo.bind("<<ComboboxSelected>>", self.ComboChange)
        self.__tipCombo.grid(row=2,column=3)
        self.__PacijentCombo.grid(row=2,column=2)
        self.__textPacijent=StringVar(self)
        self.__PacijentEntry=Entry(window, state='readonly', textvariable=self.__textPacijent)
        self.__textTip=StringVar(self)
        self.__TipEntry=Entry(window, state='readonly', textvariable=self.__textTip)

        self.__textID = StringVar(self)
        self.__IDEntry = Entry(window, state='readonly', textvariable=self.__textID)
        self.__textVreme=StringVar(self)
        self.__VremeEntry=Entry(window, state='readonly', textvariable=self.__textVreme)
        self.__textDatum = StringVar(self)
        self.__datumEntry = Entry(window, state='readonly', textvariable=self.__textDatum)
        self.__textIzvestaj = StringVar(self)
        self.__izvestajEntry = Entry(window, state=NORMAL, textvariable=self.__textIzvestaj)
        self.__textLekar = StringVar(self)
        self.__lekarEntry = Entry(window, state='readonly', textvariable=self.__textLekar)
        self.__textDicom = StringVar(self)
        self.__dicomEntry = Entry(window, state='readonly', textvariable=self.__textDicom)

        self._cyan2='cyan2'
        Label(window, text="ID: ",bg=self._cyan2).grid(row=0, column=0, sticky=E)
        self.__IDEntry.grid(row=0, column=1, sticky=E)
        Label(window, text="Pacijent: ",bg=self._cyan2).grid(row=1, column=0, sticky=E)
        self.__PacijentEntry.grid(row=1, column=1)

        Label(window, text="Datum: ",bg=self._cyan2).grid(row=2, column=0, sticky=E)
        self.__datumEntry.grid(row=2, column=1, sticky=E)
        Label(window,text="Vreme: ",bg=self._cyan2).grid(row=3,column=0,sticky=E)
        self.__VremeEntry.grid(row=3,column=1,sticky=E)

        Label(window, text="Tip: ",bg=self._cyan2).grid(row=4, column=0, sticky=E)
        self.__TipEntry.grid(row=4, column=1, sticky=E)
        Label(window, text="Izvestaj: ",bg=self._cyan2).grid(row=5, column=0, sticky=E)
        self.__izvestajEntry.grid(row=5, column=1, sticky=E)
        Label(window, text="Lekar: ",bg=self._cyan2).grid(row=6, column=0, sticky=E)
        self.__lekarEntry.grid(row=6, column=1, sticky=E)
        Label(window, text="Dicom: ",bg=self._cyan2).grid(row=7, column=0, sticky=E)
        self.__dicomEntry.grid(row=7,column=1,sticky=E)

        self.__izmeni = Button(window, text='Omoguci izmenu', command=self.OtvoriIzmenu, state=NORMAL)
        self.__izmeni.grid(row=1, column=2)
        self.__dodaj = Button(window, text='Omoguci dodavanje', command=self.bindDodaj, state=NORMAL)
        self.__dodaj.grid(row=0, column=2)
        self.__obrisiButton=Button(window, text='Obrisi snimanje',command=self.obrisiS)
        self.__dicomButton=Button(window, text='DICOM prozor',command=self.OtvoriDicom)
        self.__dicomButton.grid(row=1,column=3)

        self.__obrisiButton.grid(row=1,column=4)
        self.__nazadButton=Button(window, text='Nazad', command=self.nazad, state=NORMAL)
        self.__sviPacijentiButton=Button(window, text='Prikazi sva snimanja', command=self.svaSnimanja, state=NORMAL)
        self.__sviPacijentiButton.grid(row=3,column=2)
        self.__nazadButton.grid(row=2,column=4)
        for key in self.__pacijenti.keys():
            if self.__pacijenti[key].lbo not in self.__PacijentCombo['values']:
                imePrezime=self.__pacijenti[key].ime+" "+self.__pacijenti[key].prezime
                self.__PacijentCombo['values'] = (*self.__PacijentCombo['values'], imePrezime)


    def svaSnimanja(self):
        self.popuniListBox(self.__snimci)

    def OtvoriIzmenu(self):
        sel = self.__snimciListBox.curselection()
        if len(sel) == 0:
            return
        index = sel[0]
        id = sorted(self.__snimci)[index]
        snimak = self.__snimci[id]
        izmenaWindow=IzmenaSnimanjaWindow(self,snimak)
        izmenaWindow.mainloop()

    def ComboChange(self,event):
        trazenaSnimanja={}
        tip=self.__tipCombo.get()
        imePrezime=self.__PacijentCombo.get()
        lbo=self.searchPacijent(imePrezime).lbo
        for key in self.__snimci.keys():
            if self.__snimci[key].tip==tip and self.__snimci[key].pacijent==lbo:
                trazenaSnimanja[key]=self.__snimci[key]
        self.popuniListBox(trazenaSnimanja)

    def nazad(self):
        self.destroy()

    def OtvoriDicom(self):
        selection = self.__snimciListBox.curselection()
        if selection:
            listIndex = int(selection[0])
            id = sorted(self.__snimci)[listIndex]
            snimanje=self.__snimci[id]
            noviProzor = DicomWindow(snimanje)
            noviProzor.mainloop()
        else:
            messagebox.showerror("greska", "Mora biti selektovano snimanje!")


    def obrisiS(self):
        selection = self.__snimciListBox.curselection()
        if selection:
            if messagebox.askquestion("Upozorenje", "Da li ste sigurni da zelite da obrisete  snimanje?",
                                      icon="warning") == "yes":
                index = selection[0]
                id = sorted(self.__snimci)[index]
                del self.__snimci[id]
                Snimak.saveSnimci(self.__snimci)
                self.__snimciListBox.delete(index)
                self.__snimciListBox.selection_set(index)
        else:
            messagebox.showerror("Greska", "Niste selektovali ni jednan snimak")




    def isprazniEntry(self):
        self.__textIzvestaj.set("")
        self.__textDatum.set("")
        self.__textLekar.set("")
        self.__textID.set("")
        self.__textDicom.set("")
        self.__textVreme.set("")

    def bindDodaj(self):
        dodavanje=DodajSnimanjeWindow(self)
        dodavanje.mainloop()


    def popuniEntryPolja(self, snimak):
        self.__textID.set(snimak.id)
        self.__textDatum.set(snimak.datum)
        self.__textIzvestaj.set(snimak.izvestaj)
        self.__textLekar.set(snimak.lekar)
        self.__textTip.set(snimak.tip)
        pacijent=self.searchByLbo(snimak.pacijent)
        imePrezime=pacijent.ime+" "+pacijent.prezime
        self.__textPacijent.set(imePrezime)
        self.__textDicom.set(snimak.dicom)
        self.__textVreme.set(snimak.vreme)
    def promenaSelekcije(self, event):
        selection = self.__snimciListBox.curselection()
        if selection:
            index = int(self.__snimciListBox.curselection()[0])
            id = sorted(self.__snimci)[index]
            snimak = self.__snimci[id]
            self.popuniEntryPolja(snimak)

    def popuniListBox(self,snimci):
        self.__snimciListBox.delete(0, END)
        for keys in snimci:
            tekst = str(self.__snimci[keys].id) + ", " + self.__snimci[keys].datum + ", " +self.__snimci[keys].vreme+", "+ self.__snimci[keys].tip+", "+self.__snimci[keys].izvestaj
            self.__snimciListBox.insert(END, tekst)

    @property
    def snimci(self):
        return self.__snimci
    def searchByLbo(self,lbo):
        for keys in self.__pacijenti.keys():
            if self.__pacijenti[keys].lbo==lbo:
                return self.__pacijenti[keys]
    def searchPacijent(self,imePrezime):
        lista=imePrezime.split(" ")
        ime=lista[0]
        prezime=lista[1]
        for key in self.__pacijenti:
            if self.__pacijenti[key].ime==ime and self.__pacijenti[key].prezime==prezime:
                return self.__pacijenti[key]



