from lxml import etree
from datetime import datetime



class Pacijent:
    __fileName = "pacijenti.xml"
    def __init__ (self, lbo, ime, prezime, datum):
        self.__lbo = lbo
        self.__ime = ime
        self.__prezime = prezime
        self.__datum = datum
        self.__snimci = []

    @property
    def lbo(self):
        return self.__lbo

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, ime):
        self.__ime = ime




    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, prezime):
        self.__prezime = prezime

    @property
    def datum(self):
        return self.__datum

    @datum.setter
    def datum(self, datum):
        self.__datum = datum

    def __str__(self):
        return str(self.lbo) + ", " + self.ime + ", " + self.prezime + ", " + self.datum

    @classmethod
    def ElementToPacijent( _class, element):
        lbo = element.attrib["lbo"]
        ime = element[0].text
        datum = int(element[2].text)
        prezime = element[1].text
        pacijent = _class(lbo, ime, prezime, datum)
        return pacijent



    def createElement(self):
        element = etree.Element("pacijent")
        element.append(etree.Element("ime"))
        element.append(etree.Element("prezime"))
        element.append(etree.Element("datum"))
        element.attrib["lbo"] = self.__lbo
        element[0].text = self.__ime
        element[1].text = self.__prezime
        element[2].text = str(self.__datum)

        return element

    @classmethod
    def loadPacijenti(__class):
        xmlDoc = etree.parse(__class.__fileName)
        pacijenti = {}
        listaPacijenata = xmlDoc.getroot()
        for pacijent in listaPacijenata:
            ime = pacijent[0].text
            prezime = pacijent[1].text
            datum = pacijent[2].text
            lbo = pacijent.attrib["lbo"]
            pacijenti[lbo] = Pacijent(str(lbo), ime, prezime, datum)
        return pacijenti

    @classmethod
    def savePacijenti(_class, pacijenti):
        pacijentiElement = etree.Element("pacijenti")
        for lbo in sorted(pacijenti.keys()):
            pacijent = pacijenti[lbo]
            pacijentElement = _class.createElement(pacijent)
            pacijentiElement.append(pacijentElement)

        xmlDoc = etree.ElementTree(pacijentiElement)

        datoteka = open(_class.__fileName, "wb")
        xmlDoc.write(datoteka, encoding="UTF-8")
        datoteka.close()

