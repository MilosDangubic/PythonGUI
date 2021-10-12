from tkinter import *
from tkinter import ttk, messagebox
import pydicom as pd
import pydicom


class DicomWindow(Tk):
    def __init__(self,snimanje):
        super().__init__()
        self.addComponents()
        self.__snimanje=snimanje

    def addComponents(self):
        self.title("DICOM")
        prozor1=Frame(self, padx=5, pady=5, borderwidth=2)
        prozor1.pack(side=LEFT)
        self.__textIDP=StringVar(self)
        self.__eID=Entry(prozor1, textvariable=self.__textIDP)
        Label(prozor1, text="LBO pacijenta: ").grid(row=0, column=0, sticky=E)
        self.__eID.grid(row=0, column=1, sticky=W)

        self.__textImeiPrezimeP=StringVar(self)
        self.__eImeiPrezime=Entry(prozor1, textvariable=self.__textImeiPrezimeP)
        Label(prozor1, text="Ime i prezime pacijenta: ").grid(row=1, column=0, sticky=E)
        self.__eImeiPrezime.grid(row=1, column=1, sticky=W)

        self.__textDatumP=StringVar(self)
        self.__eDatum=Entry(prozor1,textvariable=self.__textDatumP)
        Label(prozor1, text="Datum rodjenja pacijenta: ").grid(row=2, column=0, sticky=E)
        self.__eDatum.grid(row=2, column=1, sticky=W)

        prozor2=Frame(self, padx=5, pady=5, borderwidth=2)
        prozor2.pack(side=RIGHT)

        self.__textIDpregleda=StringVar(self)
        self.__eIDpregleda=Entry(prozor2,textvariable=self.__textIDpregleda)
        Label(prozor2, text="ID pregleda: ").grid(row=0, column=0, sticky=E)
        self.__eIDpregleda.grid(row=0, column=1)

        self.__textDatumPregleda=StringVar(self)
        self.__eDatumPregleda=Entry(prozor2, textvariable=self.__textDatumPregleda)
        Label(prozor2, text="Datum pregleda: ").grid(row=1, column=0, sticky=E)
        self.__eDatumPregleda.grid(row=1, column=1, sticky=W)

        self.__textTipPregleda=StringVar(self)
        self.__eTipPregleda=Entry(prozor2,textvariable=self.__textTipPregleda)
        Label(prozor2, text="Tip pregleda: ").grid(row=2, column=0, sticky=E)
        self.__eTipPregleda.grid(row=2, column=1, sticky=W)

        self.__textdijagnozaPregleda=StringVar(self)
        self.__eDijagnozaPregleda=Entry(prozor2,textvariable=self.__textdijagnozaPregleda)
        Label(prozor2, text="Izvestaj pregleda: ").grid(row=3, column=0, sticky=E)
        self.__eDijagnozaPregleda.grid(row=3, column=1, sticky=W)

        self.__textLekarPregleda=StringVar(self)
        self.__eLekarPregleda=Entry(prozor2,textvariable=self.__textLekarPregleda)
        Label(prozor2, text="Ime lekara: ").grid(row=4, column=0, sticky=E)
        self.__eLekarPregleda.grid(row=4, column=1, sticky=W)
        self.__ucitajDicomButton=Button(prozor2,text="Otvori dicom snimak",command=self.ucitajDicom)
        self.__ucitajDicomButton.grid(row=5,column=1)

    def ucitajDicom(self):
        putanja=self.__snimanje.dicom
        if putanja=="":
            messagebox.showerror("Greska","Snimanje nema ucitan DICOM snimak")
            return
        try:
            self.__dataset=pd.read_file(putanja)
        except:
            messagebox.showerror("Greska", "Putanja do dicom snimka nevalidna")
            return
        if "PatientName" in self.__dataset:
            self.__textImeiPrezimeP.set(self.__dataset.PatientName)
        else:
            self.__eImeiPrezime['state']=DISABLED
        if "PatientID" in self.__dataset:
            self.__textIDP.set(self.__dataset.PatientID)

        if "PatientBirthDate" in self.__dataset:
            self.__textDatumP.set(self.__dataset.PatientBirthDate)


        if "StudyID" in self.__dataset:
            print(self.__dataset.StudyID)
            self.__textIDpregleda.set(self.__dataset.StudyID)


        if "Datum" in self.__dataset:
            self.__textDatumPregleda.set(self.__dataset.Datum)

        if "Modality" in self.__dataset:
            self.__textTipPregleda.set(self.__dataset.Modality)

        if "StudyDescription" in self.__dataset:
            self.__textdijagnozaPregleda.set(self.__dataset.StudyDescription)

        if "ReferringPhysiciansName" in self.__dataset:
            self.__textLekarPregleda.set(self.__dataset.ReferringPhysiciansName)
