from Database import Database
import datetime
# Import FPDF class
from fpdf import FPDF
class Lohn():
    brlohn = 0 
    ü50grund = 0
    ü50zuschl = 0
    ü100zuschl = 0 
    sv_bmg = 0 
    dienstg_sv = 0
    sv = 0
    lnk_bmg = 0
    kommst = 0
    db = 0
    dz = 0
    BV = 0
    dga = 0
    lst_bmg = 0
    lst_sb = 0
    lst = 0
    def __init__(self, monat, stundensatz, brutto,variables):
        self.monat = monat
        self.stundensatz = stundensatz
        self.brutto = brutto
        self.variables=variables[0]

    def RechnenBrlohn(self, mehr0, mehr25, mehr50, überst50, überst100, sonderz,sachbez, diäten, reisek):
        if self.stundensatz!=0:
            teiler1 = 1/(4.33*self.stundensatz)
            teiler2 = 1./143. / (self.stundensatz/38.5)
        else:
            teiler1=0
            teiler2=0
        self.brlohn = self.brutto + mehr0*(self.brutto*teiler1)*(1.+0.0)
        self.brlohn = self.brlohn + mehr25*(self.brutto*teiler1)*(1.+0.25)
        self.brlohn = self.brlohn + mehr50*(self.brutto*teiler1)*(1.+0.5)
        self.ü50grund = überst50*(self.brutto*teiler2)
        self.ü50zuschl = überst50*(self.brutto*teiler2)*0.5
        self.brlohn = self.brlohn + self.ü50grund + self.ü50zuschl
        ü100grund = überst100*(self.brutto*teiler2)
        self.ü100zuschl = überst100*(self.brutto*teiler2)
        self.brlohn = self.brlohn + ü100grund + self.ü100zuschl
        self.sv_bmg = self.brlohn + sachbez
        self.brlohn = self.brlohn + diäten
        self.brlohn = self.brlohn + reisek

    def RechnenSv(self, sachbez):
        pr20=0
        self.dienstg_sv = self.sv_bmg*0.2123
        if self.sv_bmg < self.variables[2]:
            self.sv = self.sv_bmg * 0.1512
        elif self.sv_bmg < self.variables[3]:
            self.sv = self.sv_bmg * 0.1612
        elif self.sv_bmg <self.variables[4]:
            self.sv = self.sv_bmg * 0.1712
        elif self.sv_bmg > self.variables[5]:
            self.sv = self.variables[5]*0.1812
            self.dienstg_sv = self.variables[5]*0.2123
        else:
            self.sv = self.sv_bmg*0.1812

        if sachbez != 0.0:
            pr20 = self.brlohn*0.2

            if self.sv_bmg < self.variables[2]:
                svtemp = self.sv_bmg * 0.1412
            elif self.sv_bmg < self.variables[3]:
                svtemp = self.sv_bmg * 0.1512
            elif self.sv_bmg < self.variables[4]:
                svtemp = self.sv_bmg * 0.1712
            elif self.sv_bmg > self.variables[5]:
                svtemp = self.variables[5]*0.1712
            else:
                svtemp = self.sv_bmg*0.1712
            
            if svtemp > pr20:
                
                self.dienstg_sv = self.dienstg_sv + svtemp - pr20
                if self.sv_bmg < self.variables[5]:
                    self.sv = pr20 + self.sv_bmg*0.01
        else:
            self.sv = pr20 + self.variables[5]*0.01

    def Lohn_Komm (self, diäten , reisek, sachbez, sonderz):
        self.lnk_bmg = self.brlohn - diäten - reisek + sachbez + sonderz
        self.kommst = self.lnk_bmg*0.03
        self.db = self.lnk_bmg*0.039
        self.dz = self.lnk_bmg*0.0038
        self.BV = (self.sv_bmg + sonderz)*0.0153
        self.dga = 4. * 2.

    def RechnenSvsonder(self,altesonder,sonderz):
        if (altesonder + sonderz) > self.variables[6]:
            restsonder = self.variables[6] - altesonder
            if restsonder > 0.0:
                if sonderz < self.variables[2]:
                    prsvsonder = 0.1412
                    svsonder = restsonder * 0.1412
                elif sonderz < self.variables[3]:
                    prsvsonder = 0.1512
                    svsonder = restsonder * 0.1512
                elif sonderz < self.variables[4]:
                    prsvsonder = 0.1612
                    svsonder = restsonder * 0.1612
                else:
                    prsvsonder = 0.1712
                    svsonder = restsonder*0.1712
        else:

            if sonderz < self.variables[2]:
                prsvsonder = 0.1412
                svsonder = sonderz * 0.1412
            elif sonderz < self.variables[3]:
                prsvsonder = 0.1512
                svsonder = sonderz * 0.1512
            elif sonderz < self.variables[4]:
                prsvsonder = 0.1612
                svsonder = sonderz * 0.1612
            elif sonderz > self.variables[6]:
                prsvsonder = 0.1712
                svsonder = self.variables[6]*0.1712
            else:
                prsvsonder = 0.1712
                svsonder = sonderz*0.1712
        return svsonder,prsvsonder

    def RechnenAv(self,AV_str):
        if AV_str == 1:
            AV = 41.17
        elif AV_str == 2:
            AV = 55.75
        elif AV_str > 2:
            AV = 55.75 + 18.33*(AV_str-2)
        else:
            AV = 0.
        return AV

    def RechnenU50zuschl_st(self,überst50):
        
        ü50zuschl_st = self.ü50zuschl
        ü100zuschl_st = self.ü100zuschl
        if überst50 > 10:
            ü50zuschl_st = self.ü50zuschl/überst50*10
        if self.ü50zuschl > 86.0:
            ü50zuschl_st = 86.0

        if self.ü100zuschl > 360.:
            ü100zuschl_st = 360.0
        return ü50zuschl_st,ü100zuschl_st

    def RenchLSTBMG(self,sachbez ,FBB, PP, diäten, reisek, ÖGB, überst50):

    
        if ÖGB == "Yes" or ÖGB == "YES":
            ÖGB_wert = self.brlohn*0.01
            ü50zuschl_st,ü100zuschl_st=0,0
            self.lst_bmg=0
        else:
            ÖGB_wert = 0.
        ü50zuschl_st,ü100zuschl_st = self.RechnenU50zuschl_st(überst50)
        self.lst_bmg = self.brlohn + sachbez - self.sv - FBB - PP - ü50zuschl_st - ü100zuschl_st - diäten - reisek - ÖGB_wert

    def RechnenLst_bmg_lst_sb (self,sonderz,j6, altesonder,prsvsonder,svsonder):

        # 
        if altesonder != 0.0:
            
            if altesonder < j6:
                sv_sb_teil1 = altesonder * prsvsonder
                rest_altsonder_sv = altesonder - sv_sb_teil1

                rest_altsonder_sv = max(rest_altsonder_sv - 620.0, 0.0)

                if rest_altsonder_sv < 24380.0:
                    
                    altsonder_sv = rest_altsonder_sv*0.06
                    restSB_pr = 0.06
                    restSB_lstbmg = 24380.0 - rest_altsonder_sv

                elif rest_altsonder_sv < 49380.0:

                    altsonder_sv = 24380.0*0.06 + (rest_altsonder_sv-24380.0)*0.27
                    restSB_pr = 0.27
                    restSB_lstbmg = 49380.0 - rest_altsonder_sv

                elif rest_altsonder_sv < 82713.0:

                    altsonder_sv = 24380.0*0.06 + 25000*0.27 + (rest_altsonder_sv-49380.0)*0.3575
                    restSB_pr = 0.3575
                    restSB_lstbmg = 82713.0 - rest_altsonder_sv

                else:

                    altsonder_sv = 24380.0*0.06 + 25000*0.27 + 33333.0*0.3575
                    restSB_lstbmg = 0.0
                    restSB_pr = 0.0
                    self.lst_bmg = self.lst_bmg + (rest_altsonder_sv - 83333.0)
                
                if (altesonder+sonderz)<j6:
                    if restSB_pr == 0.0:
                        self.lst_bmg = self.lst_bmg + sonderz
                    elif restSB_pr == 0.06:
                        if restSB_lstbmg >= sonderz:
                            self.lst_sb = sonderz*0.06
                        else:
                            self.lst_sb = restSB_lstbmg*0.06 + (sonderz-restSB_lstbmg)*0.27
                    elif restSB_pr == 0.27:
                        if restSB_lstbmg >= sonderz:
                            self.lst_sb = sonderz*0.27
                        else:
                            self.lst_sb = restSB_lstbmg*0.27 + (sonderz-restSB_lstbmg)*0.3575
                    elif restSB_pr == 0.3575:
                        if restSB_lstbmg >= sonderz:
                            self.lst_sb = sonderz*0.3575
                        else:
                            self.lst_sb = restSB_lstbmg*0.23575
                            self.lst_bmg = self.lst_bmg + (sonderz-restSB_lstbmg)
                else:

                    offj6 = j6 - altesonder
                    sv_sb_teil1 = offj6*prsvsonder
                    sv_sb_teil2 = svsonder - sv_sb_teil1   
                    lst_bmg_sz = offj6 - sv_sb_teil1
                    self.lst_bmg = self.lst_bmg + (sonderz - offj6) - sv_sb_teil2
                    #lst_bmg = lst_bmg + (altesonder-j6)                                             

                    if restSB_pr == 0.0:
                        self.lst_bmg = self.lst_bmg + lst_bmg_sz
                    elif restSB_pr == 0.06:
                        if restSB_lstbmg >= lst_bmg_sz:
                            self.lst_sb = lst_bmg_sz*0.06
                        else:
                            self.lst_sb = restSB_lstbmg*0.06 + (lst_bmg_sz-restSB_lstbmg)*0.27
                    elif restSB_pr == 0.27:
                        if restSB_lstbmg >= lst_bmg_sz:
                            self.lst_sb = lst_bmg_sz*0.27
                        else:
                            self.lst_sb = restSB_lstbmg*0.27 + (lst_bmg_sz-restSB_lstbmg)*0.3575
                    elif restSB_pr == 0.3575:
                        if restSB_lstbmg >= lst_bmg_sz:
                            self.lst_sb = lst_bmg_sz*0.3575
                        else:
                            self.lst_sb = restSB_lstbmg*0.23575
                            self.lst_bmg = self.lst_bmg + (lst_bmg_sz-restSB_lstbmg)


            else:

                sv_sb_teil1 = j6 * prsvsonder
                sv_sb_teil2 = altesonder*prsvsonder - sv_sb_teil1
                lst_bmg_sz = j6 - sv_sb_teil1
                self.lst_bmg = self.lst_bmg + (altesonder - j6) - sv_sb_teil2
                #lst_bmg = lst_bmg + (altesonder-j6)
                rest_altsonder_sv = j6 - sv_sb_teil1

                rest_altsonder_sv = max(rest_altsonder_sv - 620.0, 0.0)

                if rest_altsonder_sv < 24380.0:
                    
                    altsonder_sv = rest_altsonder_sv*0.06
                    restSB_pr = 0.06
                    restSB_lstbmg = 24380.0 - rest_altsonder_sv

                elif rest_altsonder_sv < 49380.0:

                    altsonder_sv = 24380.0*0.06 + (rest_altsonder_sv-24380.0)*0.27
                    restSB_pr = 0.27
                    restSB_lstbmg = 49380.0 - rest_altsonder_sv

                elif rest_altsonder_sv < 82713.0:

                    altsonder_sv = 24380.0*0.06 + 25000*0.27 + (rest_altsonder_sv-49380.0)*0.3575
                    restSB_pr = 0.3575
                    restSB_lstbmg = 82713.0 - rest_altsonder_sv

                else:

                    altsonder_sv = 24380.0*0.06 + 25000*0.27 + 33333.0*0.3575
                    restSB_lstbmg = 0.0
                    restSB_pr = 0.0
                    self.lst_bmg = self.lst_bmg + (rest_altsonder_sv - 83333.0)
                
                if restSB_pr == 0.0:
                    self.lst_bmg = self.lst_bmg + sonderz
                elif restSB_pr == 0.06:
                    if restSB_lstbmg >= sonderz:
                        self.lst_sb = sonderz*0.06
                    else:
                        self.lst_sb = restSB_lstbmg*0.06 + (sonderz-restSB_lstbmg)*0.27
                elif restSB_pr == 0.27:
                    if restSB_lstbmg >= sonderz:
                        self.lst_sb = sonderz*0.27
                    else:
                        self.lst_sb = restSB_lstbmg*0.27 + (sonderz-restSB_lstbmg)*0.3575
                elif restSB_pr == 0.3575:
                    if restSB_lstbmg >= sonderz:
                        self.lst_sb = sonderz*0.3575
                    else:
                        self.lst_sb = restSB_lstbmg*0.23575
                        self.lst_bmg = self.lst_bmg + (sonderz-restSB_lstbmg) 

        else:
                
            if j6 > sonderz:
                lst_bmg_sz = sonderz - svsonder
                
                lst_bmg_sz = lst_bmg_sz - 620.

                if lst_bmg_sz < 24380.0:
                    self.lst_sb = lst_bmg_sz*0.06
                else:
                    if lst_bmg_sz < 49380.0:
                        self.lst_sb = 24380.0*0.06 + (lst_bmg_sz-24380.0)*0.27
                    else:
                        if lst_bmg_sz < 83333.0:
                            self.lst_sb = 24380.0*0.06 + 25000*0.27 + (lst_bmg_sz-49380.0)*0.3575
                        else:
                            self.lst_sb = 24380.0*0.06 + 25000*0.27 + 33333.0*0.3575
                            self.lst_bmg = self.lst_bmg + (lst_bmg_sz - 83333.0)
            else:

                sv_sb_teil1 = j6 * prsvsonder
                sv_sb_teil2 = svsonder - sv_sb_teil1
                lst_bmg_sz = j6 - sv_sb_teil1
                self.lst_bmg = self.lst_bmg + (sonderz - j6) - sv_sb_teil2
                
                lst_bmg_sz = lst_bmg_sz - 620.

                if lst_bmg_sz < 24380.0:
                    self.lst_sb = lst_bmg_sz*0.06
                else:
                    if lst_bmg_sz < 49380.0:
                        self.lst_sb = 24380.0*0.06 + (lst_bmg_sz-24380.0)*0.27
                    else:
                        if lst_bmg_sz < 83333.0:
                            self.lst_sb = 24380.0*0.06 + 25000*0.27 + (lst_bmg_sz-49380.0)*0.3575
                        else:
                            self.lst_sb = 24380.0*0.06 + 25000*0.27 + 33333.0*0.3575
                            self.lst_bmg = self.lst_bmg + (lst_bmg_sz - 83333.0)
    def RechnenLst(self,AV,FaBoP,PEur):
        if self.lst_bmg < 927.67:
            self.lst = 0.
        elif self.lst_bmg < 1511.00:
            self.lst = self.lst_bmg*0.2 - self.variables[7] - 33.33
        elif self.lst_bmg < 2594.33:
            self.lst = self.lst_bmg*self.variables[8] - self.variables[9] - 33.33
        elif self.lst_bmg < 5011.33:
            self.lst = self.lst_bmg*0.42 - self.variables[10] - 33.33
        elif self.lst_bmg < 7511.0:
            self.lst = self.lst_bmg*0.48 - self.variables[11] - 33.33
        elif self.lst_bmg < 83344.33:
            self.lst = self.lst_bmg*0.5 - self.variables[12]  - 33.33
        else:
            self.lst = self.lst_bmg*0.55 -self.variables[13] - 33.33

        self.lst = max(self.lst - FaBoP - PEur - AV,0.0)

    def RechnenNetto (self):
        netto = self.brlohn - self.sv - self.lst
        return netto
    def SV_Dienstgeberbeitrag (self,sonderz,svsonder):
        dienstg_svsonder = sonderz*0.2073
        return self.dienstg_sv + dienstg_svsonder
    def Gehaltsabrechnung(self,sonderz,svsonder,loko_id):
        sobz = sonderz - svsonder - self.lst_sb
        self.sv_dienstgeberbeitrag=self.SV_Dienstgeberbeitrag(sonderz,svsonder)
        self.netto= self.RechnenNetto()
        db = Database('LOKO.db')
        db.insert_Gehaltsabrechnung(loko_id,self.netto,self.sv_bmg,self.sv, self.lst_bmg,self.lst,sobz,svsonder,self.lst_sb,self.kommst,self.dga,self.db,self.dz,self.sv_dienstgeberbeitrag,self.BV)
        print(f"Der Nettolohn lt Berechnung (2021) ist: {self.netto}\n")
        print(f"SV_Bmg: {self.sv_bmg}€    SV lfd: {self.sv}€\n Lst_Bmg: {self.lst_bmg}€   Lohnsteuer: {self.lst}€")    
        # Der sonstige Bezug (netto) ist:
        print(f"Der sonstige Bezug (netto) ist: {sobz}")
        # SV-Sonstiger Bezug
        print(f"SV-Sonstiger Bezug:: {svsonder}€   Lohnsteuer-Sonstiger Bezug: {self.lst_sb}")
        # Lohnnebenkosten\nKommunlasteuer:        
        print(f"Lohnnebenkosten\nKommunlasteuer: {self.kommst}€   U-bahnsteuer: {self.dga}€   Dienstbeitrag: {self.db}€    Zuschlag (DB): {self.dz}€   SV-Dienstgeberbeitrag: {self.sv_dienstgeberbeitrag}€   BV: {self.BV}€")
        
    def create_pdf(self,loko,person,sonderz,svsonder,date):
        sobz = sonderz - svsonder - self.lst_sb
        self.sv_dienstgeberbeitrag=self.SV_Dienstgeberbeitrag(sonderz,svsonder)
        self.netto= self.RechnenNetto()
        db = Database('LOKO.db')
        db.insert_Gehaltsabrechnung(loko[1],self.netto,self.sv_bmg,self.sv, self.lst_bmg,self.lst,sobz,svsonder,self.lst_sb,self.kommst,self.dga,self.db,self.dz,self.sv_dienstgeberbeitrag,self.BV,date)

        # Create instance of FPDF class
        # Letter size paper, use inches as unit of measure
        pdf=FPDF(format='letter', unit='in')
        
        # Add new page. Without this you cannot create the document.
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)        
        # set font
        pdf.set_font('DejaVu','',10.0) 
        
        # Effective page width, or just epw
        epw = pdf.w - 2*pdf.l_margin
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
        col_width = epw/4
        
        # Since we do not need to draw lines anymore, there is no need to separate
        # headers from data matrix.

        data = [
        ["Ausgabetag", date],
        [],
        ["Mitarbeiterinformation"],
        ["First Name", "Last Name","Birth Date"],
        [person[1], person[2],person[3]],
        [],
        ["Berufsinformation"],
        ["Brutto", "Stundensatz","Monat"],
        [loko[3], loko[4],loko[5]],
        [],
        ['Der Nettolohn ',self.netto],
    
        ['SV_Bmg',u"""{}€""".format(self.sv_bmg),"SV lfd",u"""{}€""".format(self.sv)],
        ["Lst_Bmg",u"""{}€""".format(self.lst_bmg),"Lohnsteuer",u"""{}€""".format(self.lst)],
        ['Der sonstige Bezug(Netto)',u"""{}€""".format(sobz)],
        ['SV-Sonstiger Bezug',u"""{}€""".format(svsonder),"Lohnsteuer-Sonstiger Bezug",u"""{}€""".format(self.lst_sb)],
        ['Lohn/Kommunlasteuer',u"""{}€""".format(self.kommst),"U-bahnsteuer",u"""{}€""".format(self.dga)],
        ['Dienstbeitrag',u"""{}€""".format(self.db),"Zuschlag (DB)",u"""{}€""".format(self.dz)],
        ['SV-Dienstgeberbeitrag',u"""{}€""".format(self.sv_dienstgeberbeitrag),"BV",u"""{}€""".format(self.BV)]
        ]
        
        # Document title centered, 'B'old, 14 pt
        pdf.set_font('DejaVu','',14.0) 
        pdf.cell(epw, 0.0, 'Gehaltsabrechnung', align='C')
        pdf.set_font('DejaVu','',10.0) 
        pdf.ln(0.5)
        
        # Text height is the same as current font size
        th = pdf.font_size
        
        
        # Line break equivalent to 4 lines
        pdf.ln(2*th)
        
        
        # Here we add more padding by passing 2*th as height
        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        # create timestamp
        t=datetime.datetime.now()
        # create pdf file name
        # pdf file name contains employee name and timestamp
        file_name='{}-{}-{}-{}-{}-{}-{}.pdf'.format(person[2],t.year,t.month,t.day,t.hour,t.minute,t.second)
        # create pdf with this name
        pdf.output(file_name,'F')











