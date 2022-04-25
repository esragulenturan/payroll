from AbrechnungClass import Lohn
from Database import Database
# create a object from database class
db = Database('LOKO.db')
firstname = input("Geben Sie den firstname des Mitarbeiters ein")
surname = input("Geben Sie den surname des Mitarbeiters ein")
birthdate = input("Geben Sie das Geburtsdatum des Mitarbeiters ein")
# insert person data to PERS table
db.insert_person(firstname, surname, birthdate)
# save person id for insert in other table
person_id=db.person_id
monat = int(input("Gib den Monat als Zahl an:\n"))
stundensatz = float(input("Gib die Arbeitsstunden/Woche an:\n"))
brutto = float(input("Gib Bruttolohn ein:\n"))
# insert lohn konto information in LOKO table
db.insert_loko(person_id,monat,stundensatz,brutto)
mehr0 = float(input("Gib Mehrstunden mit 0% ein:\n"))
mehr25 = float(input("Gib Mehrstunden mit 25% ein:\n"))
mehr50 = float(input("Gib Mehrstunden mit 50% ein:\n"))
überst50 = float(input("Gib Überstunden mit 50% ein:\n"))
überst100 = float(input("Gib Überstunden mit 100% ein:\n"))
sonderz = float(input("Gib Sonderzahlung ein:\n"))
sachbez = float(input("Gib Sachbezug ein:\n"))
diäten = float(input("Gib Diäten (km-, Verpflegungsgeld) ein:\n"))
reisek = float(input("Gib die Reisekosten (Tag- und Nachtgeld) ein:\n"))
# create object from Lohn class
l=Lohn(monat, stundensatz, brutto)
l.RechnenBrlohn(mehr0, mehr25, mehr50, überst50, überst100, sonderz,sachbez, diäten, reisek)
l.RechnenSv(sachbez)
l.Lohn_Komm (diäten , reisek, sachbez, sonderz)
if sonderz != 0.:
    altesonder = float(input("Gib das Brutto der Sonderzahlungen des bisherigen Jahres ein:\n"))
    svsonder,prsvsonder = l.RechnenSvsonder(altesonder,sonderz)
else:
    altesonder = 0
    svsonder,prsvsonder = 0.


FBB = float(input("Gib den Freibetragsbescheid an:\n"))

PP = float(input("Gib die Pendlerpauschale an:\n"))
PEur = float(input("Gib den Pendlereuro ein:\n"))

AV_str = int(input("Besteht AlleinVerdiener-/AlleinErzieheranspruch? (Anzahl der Kinder)\n"))
AV = l.RechnenAv(AV_str)


FaBoP_str = input("Besteht Anspruch auf den Familienbonus? (y/n)\n")
FaBoP = 0.0
u18g=0
u18h=0
if FaBoP_str == "y":
    u18g = int(input("Wie viele Kinder unter 18 mit ganzem Anspruch? (Anzahl)\n"))
    u18h= int(input("Wie viele Kinder unter 18 mit halbem Anspruch? (Anzahl)\n"))
    ü18g = int(input("Wie viele Kinder über 18 mit ganzem Anspruch? (Anzahl)\n"))
    ü18h = int(input("Wie viele Kinder über 18 mit halbem Anspruch? (Anzahl)\n"))
    FaBoP = u18g * 125.0 + u18h * 62.5 + ü18g * 41.68 + ü18h * 20.84
    

ÖGB = input("Ist der Arbeiter/Angestellte Gewerkschaftsmitglied? (y/n):\n")

if sonderz != 0.:
    j6 = float(input("Gib das aktuelle Jahressechstel (J/6) an:\n"))
    l.RechnenLst_bmg_lst_sb(sachbez ,FBB, PP, diäten, reisek, ÖGB, sonderz,j6, altesonder,prsvsonder,überst50)
   
else:
    self.lst_sb = 0.

# save loko id for insert in other table
loko_id=db.loko_id
# insert this information to INFO table that get them above
db.insert_information(loko_id,mehr0,mehr25,mehr50,überst50,überst100,sonderz,sachbez,diäten,reisek,FBB,PP,PEur,u18g,u18h,j6)

l.RechnenLst(AV,FaBoP,PEur)

l.Gehaltsabrechnung(sonderz,svsonder,loko_id)


input("Zum Beenden beliebige Taste drücken!")