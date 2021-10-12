from  tkinter import *

class SnimanjaPacijentaWindow(Tk):
    def __init__(self,snimci):
        super().__init__()
        self.__snimci = snimci
        self.addComponents()
        self.popuniListBox()

    def addComponents(self):
        self.__snimciListBox = Listbox(self, width=40)
        self.__snimciListBox.pack(side=RIGHT)
        title = "Snimci"
        self.title(title)
        self.__snimciListBox.bind("<<ListboxSelect>>", self.promenaSelekcije)
        window = Frame(self)
        window.pack(side=LEFT, fill=BOTH, expand=1)
        self.__textPacijent = StringVar(self)
        self.__PacijentEntry=Entry(window, state='readonly', textvariable=self.__textPacijent)
        self.__textTip=StringVar(self)
        self.__TipEntry=Entry(window, state='readonly', textvariable=self.__textTip)
        self.__textID = StringVar(self)
        self.__IDEntry = Entry(window, state='readonly', textvariable=self.__textID)
        self.__textVreme = StringVar(self)
        self.__VremeEntry = Entry(window, state='readonly', textvariable=self.__textVreme)
        self.__textDatum = StringVar(self)
        self.__datumEntry = Entry(window, state='readonly', textvariable=self.__textDatum)
        self.__textIzvestaj = StringVar(self)
        self.__izvestajEntry = Entry(window, state='readonly', textvariable=self.__textIzvestaj)
        self.__textLekar = StringVar(self)
        self.__lekarEntry = Entry(window, state='readonly', textvariable=self.__textLekar)
        self.__textDicom = StringVar(self)
        self.__dicomEntry = Entry(window, state='readonly', textvariable=self.__textDicom)

        Label(window, text="ID: ").grid(row=0, column=0, sticky=E)
        self.__IDEntry.grid(row=0, column=1, sticky=E)
        Label(window, text="LBO: ").grid(row=1, column=0, sticky=E)
        self.__PacijentEntry.grid(row=1, column=1)
        Label(window, text="Datum: ").grid(row=2, column=0, sticky=E)
        self.__datumEntry.grid(row=2, column=1, sticky=E)
        Label(window, text="Vreme: ").grid(row=3, column=0, sticky=E)
        self.__VremeEntry.grid(row=3, column=1, sticky=E)

        Label(window, text="Tip: ").grid(row=4, column=0, sticky=E)
        self.__TipEntry.grid(row=4, column=1, sticky=E)
        Label(window, text="Izvestaj: ").grid(row=5, column=0, sticky=E)
        self.__izvestajEntry.grid(row=5, column=1, sticky=E)
        Label(window, text="Lekar: ").grid(row=6, column=0, sticky=E)
        self.__lekarEntry.grid(row=6, column=1, sticky=E)
        Label(window, text="Dicom: ").grid(row=7, column=0, sticky=E)
        self.__dicomEntry.grid(row=7, column=1, sticky=E)

    def promenaSelekcije(self, event):
        selection = self.__snimciListBox.curselection()
        if selection:
            index = int(self.__snimciListBox.curselection()[0])
            id = sorted(self.__snimci)[index]
            snimak = self.__snimci[id]
            self.popuniEntryPolja(snimak)

    def popuniListBox(self):
        self.__snimciListBox.delete(0, END)
        for keys in self.__snimci:
            tekst = str(self.__snimci[keys].id) + ", " + self.__snimci[keys].datum + ", " + self.__snimci[
                keys].vreme + ", " + self.__snimci[keys].tip + ", " + self.__snimci[keys].izvestaj
            self.__snimciListBox.insert(END, tekst)

    def popuniEntryPolja(self, snimak):
        self.__textID.set(snimak.id)
        self.__textDatum.set(snimak.datum)
        self.__textIzvestaj.set(snimak.izvestaj)
        self.__textLekar.set(snimak.lekar)
        self.__textPacijent.set(snimak.pacijent)
        self.__textTip.set(snimak.tip)
        self.__textDicom.set(snimak.dicom)
        self.__textVreme.set(snimak.vreme)