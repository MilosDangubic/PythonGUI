from lxml import etree
class Snimak:
    __ID = 0
    __fileName = "snimanja.xml"
    def __init__(self, id,pacijent, datum, tip,izvestaj, lekar,dicom,vreme):
        self.__id = id
        self.__datum =datum
        self.__vreme=vreme
        self.__izvestaj=izvestaj
        self.__tip = tip
        self.__lekar=lekar
        self.__pacijent=pacijent
        self.__dicom=dicom

    @property
    def dicom(self):
        return self.__dicom

    @dicom.setter
    def dicom(self, dicom):
        self.__dicom =dicom

    @property
    def vreme(self):
        return self.__vreme

    @vreme.setter
    def vreme(self, vreme):
        self.__vreme = vreme
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id
    @property
    def pacijent(self):
        return self.__pacijent

    @property
    def datum(self):
        return self.__datum

    @datum.setter
    def datum(self, datum):
        self.__datum = datum

    @property
    def izvestaj(self):
        return self.__izvestaj

    @izvestaj.setter
    def izvestaj(self, izvestaj):
        self.__izvestaj = izvestaj

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, tip):
        self.__tip = tip

    @property
    def lekar(self):
        return self.__lekar


    @lekar.setter
    def lekar(self, lekar):
        self.__lekar = lekar

    @classmethod
    def getSnimakFromElement(_class, element):
        ID = int(element.attrib["id"])
        pacijent = element[0].text
        datum = element[1].text
        tip = element[2].text
        izvestaj=element[3].text
        lekar=element[4].text
        dicom=element[5].text
        vreme=element[6].text
        snimak = _class(ID, pacijent, datum, tip,izvestaj,lekar,dicom,vreme)
        return snimak

    @classmethod
    def loadSnimci(_class):
        xmlDoc = etree.parse(_class.__fileName)
        snimci = {}

        snimciElement = xmlDoc.getroot()
        for snimakElem in snimciElement:
            snimak = _class.getSnimakFromElement(snimakElem)
            snimci[snimak.id] = snimak
        return snimci

    @classmethod
    def createElement(self,s):
        element = etree.Element("snimak")
        element.attrib["id"] = str(s.id)
        element.append(etree.Element("pacijent"))
        element.append(etree.Element("datum"))
        element.append(etree.Element("tip"))
        element.append(etree.Element("izvestaj"))
        element.append(etree.Element("lekar"))
        element.append(etree.Element("dicom"))
        element.append(etree.Element("vreme"))
        element[0].text = str(s.pacijent)
        element[1].text = str(s.datum)
        element[2].text = str(s.tip)
        element[3].text = s.izvestaj
        element[4].text = s.lekar
        element[5].text=s.dicom
        element[6].text=s.vreme
        return element

    @classmethod
    def saveSnimci(_class, snimci):
        snimciElement = etree.Element("snimanja")
        for id in sorted(snimci.keys()):
            snimak = snimci[id]
            snimakEl = _class.createElement(snimak)
            snimciElement.append(snimakEl)
        xmlDoc = etree.ElementTree(snimciElement)
        datoteka = open(_class.__fileName, "wb")
        xmlDoc.write(datoteka, encoding="UTF-8")
        datoteka.close()