from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pacijent import *
from snimanja import *
from  datetime import datetime
from DicomWindow import  *
from SnimanjaPacijentaWindow import *
import  SnimanjaWindow
import IzmenaWindow
import DodajPacijentaWindow


class PacijentWindow(Tk):

    def __init__(self):
        super().__init__()
        self.__pacijenti = Pacijent.loadPacijenti()
        self.__snimci=Snimak.loadSnimci()
        self.addComponents()
        self.fillListBox(self.__pacijenti)

    @property
    def pacijenti(self):
        return self.__pacijenti


    def addComponents(self):
        self.title("Pacijenti")
        self._cyan3='cyan3'
        window = Frame(self, padx=5, pady=5, borderwidth=2,background= self._cyan3)
        window.pack(side=RIGHT)

        self.__pacijentiListbox = Listbox(self,width=40)
        self.__pacijentiListbox.pack(side=LEFT)
        self.__pacijentiListbox.bind("<<ListboxSelect>>",self.selectionChange)


        self.__textLBO = StringVar(self)
        self.__LBOEntry = Entry(window,state = 'readonly', textvariable = self.__textLBO,)
        self.__textIme = StringVar(self)
        self.__imeEntry = Entry(window,state = 'readonly',textvariable = self.__textIme)
        self.__textPrezime = StringVar(self)
        self.__prezimeEntry = Entry(window,state = 'readonly',textvariable = self.__textPrezime)
        self.__textDatum = StringVar(self)
        self.__DatumEntry = Entry(window,state = 'readonly',textvariable = self.__textDatum)
        self.__textSearch = StringVar(self)
        self.__textSearch.trace("w", lambda name, index, mode, sv=self.__textSearch: self.search(sv))

        self._cyan2='cyan2'
        self._write='write'

        self.__searchEntry = Entry(window, state=NORMAL, textvariable=self.__textSearch)
        Label(window,text="Ime: ",bg=self._cyan2).grid(row=0,column=0,sticky=E)
        self.__imeEntry.grid(row=0,column=1,sticky=W)
        Label(window,text="Prezime: ",bg=self._cyan2).grid(row=1,column=0,sticky=E)
        self.__prezimeEntry.grid(row=1,column=1,sticky=W)
        Label(window,text="LBO: ",bg=self._cyan2).grid(row=2,column=0,sticky=E)
        self.__LBOEntry.grid(row=2,column=1,sticky=W)
        Label(window,text="Datum rodjenja:",bg=self._cyan2).grid(row=3,column=0,sticky=E)
        self.__DatumEntry.grid(row=3,column=1,sticky=W)
        Label(window,text="Search: ",bg=self._cyan2).grid(row=4,column=0,sticky=E)
        self.__searchEntry.grid(row = 4, column = 1, sticky = E)


        self.__btnomoguciIzmenu = Button(window, text = 'Omoguci izmenu', command = self.omoguciIzmenu, state = NORMAL)
        self.__btnomoguciIzmenu.grid(row = 5, column = 0, sticky = E)

        self.__btnDodaj = Button(window,text = 'Omoguci dodavanje',command=self.dodajPacijenta, state = NORMAL)
        self.__btnDodaj.grid(row=5, column=2, sticky=E)

        self.__btnObrisi = Button(window, text='Obriši pacijenta', command=self.obrisiPacijenta, state=NORMAL)
        self.__btnObrisi.grid(row=6, column=0, sticky=SW)
        self.__btnSnimanja = Button(window, text='Snimanja pacijenta',command=self.OtvoriSnimanja, state=NORMAL)
        self.__btnSnimanja.grid(row=6,column=1)
        self.__btnOsvezi = Button(window, text = "Osveži", command = self.osvezavajne, state = NORMAL)
        self.__btnOsvezi.grid(row = 6, column = 7, sticky=W)
        self.__btnNazad = Button(window, text="Nazad", command=self.nazad, state=NORMAL)
        self.__btnNazad.grid(row=5, column=1, sticky=E)

    def OtvoriSnimanja(self):
        selection = self.__pacijentiListbox.curselection()
        if selection:
            listIndex = int(selection[0])
            LBO = sorted(self.__pacijenti)[listIndex]
            pacijent = self.__pacijenti[LBO]
            snimanja=self.pacijentSnimak(pacijent)
            win=SnimanjaPacijentaWindow(snimanja)
            win.mainloop()


    def osvezavajne(self):
        pacijenti = Pacijent.loadPacijenti()
        self.fillListBox(pacijenti)


    def pacijentSnimak(self,pacijent):
        snim={}
        for key in self.__snimci:
            if self.__snimci[key].pacijent==pacijent.lbo:
                snim[self.__snimci[key].id]=self.__snimci[key]
        return  snim


    def fillListBox(self,lista):
        self.__pacijentiListbox.delete(0,END)
        for lbo in sorted(lista):
            p = lista[lbo]
            ps = p.prezime+", "+p.ime+", "+p.lbo+" "+p.datum
            self.__pacijentiListbox.insert(END, ps)



    def selectionChange(self,event):
        selection = self.__pacijentiListbox.curselection()
        if selection:
            listIndex = int(selection[0])
            LBO = sorted(self.__pacijenti)[listIndex]
            pacijent = self.__pacijenti[LBO]
            self.popuniEntryPolja(pacijent)

    def popuniEntryPolja(self, pacijent):
        self.__textLBO.set(pacijent.lbo)
        self.__textIme.set(pacijent.ime)
        self.__textPrezime.set(pacijent.prezime)
        self.__textDatum.set(pacijent.datum)

    def omoguciIzmenu(self):
        zaIzmenu = self.__pacijentiListbox.curselection()
        if zaIzmenu:
            index = zaIzmenu[0]
            lbo = sorted(self.__pacijenti)[index]
            izmena =IzmenaWindow.IzmenaWindow(lbo,self)
            izmena.mainloop()
        else:
            messagebox.showwarning("Upozorenje", "Niste selektovali pacijenta za izmenu!")
            return








    def dodajPacijenta(self):
        dodajPacijenta = DodajPacijentaWindow.DodajPacijentaWindow(self)
        dodajPacijenta.mainloop()


    def obrisiEntryPolja(self):
        self.__textLBO.set("")
        self.__textIme.set("")
        self.__textPrezime.set("")
        self.__textDatum.set("")


    def obrisiPacijenta(self):
        selection= self.__pacijentiListbox.curselection()
        if selection:
            if messagebox.askquestion("Upozorenje", "Da li ste sigurni da zelite da obrisete  pacijenta?",
                                  icon="warning") == "yes":
                index = selection[0]
                lbo = sorted(self.__pacijenti)[index]
                del self.__pacijenti[lbo]
                keys=[]
                for k in self.__snimci.keys():
                    if self.__snimci[k].pacijent==lbo:
                        keys.append(k)
                for k in keys:
                    del self.__snimci[k]
                Pacijent.savePacijenti(self.__pacijenti)
                Snimak.saveSnimci(self.__snimci)
                self.__pacijentiListbox.delete(index)
                self.__pacijentiListbox.selection_set(index)
                self.obrisiEntryPolja()
        else:
            messagebox.showerror("Greska","Niste selektovali ni jednog pacijenta")

    def search(self,param):
       # deo = self.__textSearch.get()
        deo=param.get()
        provera = False
        index = 0
        pretraga={}
        for key in self.__pacijenti:
            if len(deo) != 0 and deo.lower() in  self.__pacijenti[key].ime.lower():
                pretraga[key]=self.__pacijenti[key]
            if len(deo) != 0 and deo.lower() in  self.__pacijenti[key].prezime.lower():
                pretraga[key] = self.__pacijenti[key]
        if len(deo)==0:
           self.fillListBox(self.__pacijenti)
        else:
            values = []
            for key in pretraga.keys():
                values.append(pretraga[key])
            for i in range(len(values) - 1):
                for j in range(i + 1, len(values)):
                    if values[j].prezime < values[i].prezime:
                        t = values[i]
                        values[i] = values[j]
                        values[j]=t
            pretraga = {}
            for v in values:
                pretraga[v.lbo] = v
            self.fillListBox(pretraga)


    def nazad(self):
        self.destroy()
