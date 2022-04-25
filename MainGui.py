from AbrechnungClass import Lohn
from Database import Database
from tkinter import *                  
from tkinter import ttk
from tkcalendar import DateEntry
db = Database('LOKO.db')
# this function enable or disable altesonder and j6 input
def on_key_press_sonderz(event):
       n=entry_sonderz.get()
       # if sonders is 0 or empty,disable altesonder and j6 input
       if n=="" or n==0:
              entry_altesonder.config(state= "disabled")
              lbl_altesonder.config(state= "disabled")
              lbl_j6.config(state= "disabled")
              entry_j6.config(state= "disabled")
              return 0
       n=int(n)
       # if sonders is greater than zero,disable altesonder and j6 input
       if n>0:
              entry_altesonder.config(state= "normal")
              lbl_altesonder.config(state= "normal")
              lbl_j6.config(state= "normal")
              entry_j6.config(state= "normal")
              
# enable or disable u18g,u18h,... entry            
def  FaBoP_str_combo_selected(event):
       f=FaBoP_var.get()
       # if familienbounce is no disable u18g,u18h,... input
       if f=="No":
              lbl_u18g.config(state="disabled")
              entry_u18g.config(state="disabled")
              lbl_u18h.config(state="disabled")
              entry_u18h.config(state="disabled")
              lbl_u_18g.config(state="disabled")
              entry_u_18g.config(state="disabled")
              lbl_u_18h.config(state="disabled")
              entry_u_18h.config(state="disabled")
       # if familienbounce is yes disable u18g,u18h,... input
       if f =="Yes":
              lbl_u18g.config(state="normal")
              entry_u18g.config(state="normal")
              lbl_u18h.config(state="normal")
              entry_u18h.config(state="normal")
              lbl_u_18g.config(state="normal")
              entry_u_18g.config(state="normal")
              lbl_u_18h.config(state="normal")
              entry_u_18h.config(state="normal")

# register a person in database      
def register_person():
       # global variables
       global person_list,person_var
       # get information from entry
       firstname= entry_fname.get()
       surname= entry_lname.get()
       birthdate= cal.get()
       # insert person data to PERS table
       db.insert_person(firstname, surname, birthdate)
       # select all person from database
       person_list = db.select_all_persons()
       # grid option box in tab2. 
       # update it for show new person
       person_combo= OptionMenu(f2, person_var, *person_list)
       person_combo.grid(row=0,column=1)
 

      

def register_loko():
       global loko_list,loko_var
       # The loko selected in the option box.
       p=person_var.get()
       # split this stroing from "."
       p=p.split(".")
       # save person id from splited string
       person_id= int(p[0])
       # get information from entry
       monat=float(entry_monat.get())
       stundensatz = float(entry_stundensatz.get())
       brutto = float(entry_brutto.get())
       # insert lohn konto information in LOKO table
       db.insert_loko(person_id,monat,stundensatz,brutto)
       # select all loko from database
       loko_list = db.select_all_loko()
        # grid option box in tab3. 
       # update it for show new loko
       person_combo= OptionMenu(frame_search, loko_var, *loko_list)
       person_combo.grid(row=0,column=3)


def registe_info():
       # save the year based on which we want the payroll to be calculated.
       year=year_option_var.get()
       # Select the employee account.
       l=loko_var.get()
       # split employee account string from " " and convert it to list
       l=l.split(" ")
       # fetch loko id from this list  
       loko_id= int(l[2])
       # fetch this loko information from database
       loko=db.select_loko_with_id(loko_id)
       print(loko)
       # save loko information in variables
       brutto=loko[0][3]
       stundensatz=loko[0][4]
       monat=loko[0][5]
       # get data from tab3 form 
       mehr0=float(entry_mehr0.get())
       mehr25=float(entry_mehr25.get())
       mehr50=float(entry_mehr50.get())
       überst50=float(entry_uberst50.get())
       überst100=float(entry_uberst100.get())
       sonderz=float(entry_sonderz.get())
       sachbez=float(entry_sachbez.get())
       diäten=float(entry_diaten.get())
       reisek=float(entry_reisek.get())
       # for the year chosen by the user, fetch the variable numbers in the formulas from the database. 
       variables= db.select_variables_based_year(year)
       # create object from Lohn class
       l=Lohn(monat, stundensatz, brutto,variables)
       # calculate Brlohn
       l.RechnenBrlohn(mehr0, mehr25, mehr50, überst50, überst100, sonderz,sachbez, diäten, reisek)
       # calculate sv
       l.RechnenSv(sachbez)
       # calculate Lohn_Komm
       l.Lohn_Komm (diäten , reisek, sachbez, sonderz)
       if sonderz != 0.:
              altesonder = float(entry_altesonder.get())
              svsonder,prsvsonder = l.RechnenSvsonder(altesonder,sonderz)
       else:
              altesonder = 0
              svsonder=0
              prsvsonder = 0.
       # get data from tab3 form 
       FBB = float(entry_fbb.get())

       PP = float(entry_pp.get())
       PEur = float(entry_PEur.get())

       AV_str = int(entry_av.get())
       # calculate Av
       AV = l.RechnenAv(AV_str)
       FaBoP_str = FaBoP_var.get()
       FaBoP = 0.0
       u18g=0
       u18h=0
       if FaBoP_str == "Yes":
              if entry_u18g.get()=="":
                     u18g=0
              else:
                     u18g = int(entry_u18g.get())
              if entry_u18h.get()=="":
                     u18h=0
              else:
                     u18h= int(entry_u18h.get())
              if entry_u_18g.get()=="":
                     ü18g=0
              else:
                     ü18g = int(entry_u_18g.get())
              if entry_u_18h.get()=="":
                     ü18h=0
              else:
                     ü18h = int(entry_u_18h.get())
              FaBoP = u18g * variables[0][14] + u18h * 62.5 + ü18g * 41.68 + ü18h * 20.84
              

       ÖGB = ogb_var.get()
       j6=0
       l.RenchLSTBMG(sachbez ,FBB, PP, diäten, reisek, ÖGB, überst50)
       if sonderz != 0.:
              if entry_j6.get()=="":
                     j6=0
              else:
                     j6 = float(entry_j6.get())
              # calculate lst_bmg and lst_sb
              l.RechnenLst_bmg_lst_sb(sachbez ,FBB, PP, diäten, reisek, ÖGB, sonderz,j6, altesonder,prsvsonder,überst50,svsonder)
              
       else:
              lst_sb = 0.

       # insert this information to INFO table that get them above
       db.insert_information(loko_id,mehr0,mehr25,mehr50,überst50,überst100,sonderz,sachbez,diäten,reisek,FBB,PP,PEur,u18g,u18h,j6)
       # calculate lst
       l.RechnenLst(AV,FaBoP,PEur)

       # l.Gehaltsabrechnung(sonderz,svsonder,loko_id)
       # select person information from database
       person=db.select_person_with_id(loko[0][0])
       # get date from tab3 form
       date=cal_payrol.get()
       # save payroll In pdf format in the current folder
       l.create_pdf(loko[0],person[0],sonderz,svsonder,date)
# show payroll in gui
def show_payrol():
       # get selected loko from tab3 form
       l=loko_var.get()
       # split this string fro " " and convert it to list
       l=l.split(" ")
       # select loko id from list
       loko_id= int(l[2])
       # get date from tab3 form
       date=cal_payrol.get()
       # search geh information from database
       # find this loko payroll that registered in this date
       geh=db.select_geh(loko_id,date)
       # if geh is not empty
       if len(geh)!=0:
              # fetch geh data
              geh=geh[0]
              print(geh)
              # fetch loko information from database
              loko=db.select_loko_with_id(geh[1])
              # select person information from database
              person=db.select_person_with_id(loko[0][0])

              # show payroll information in tkinter
              ##################
              # payroll window #
              ##################
              win=Toplevel(root)
              lbl_date=Label(win,text="Ausgabetag",pady=5)
              lbl_date.grid(row=0,column=0)
              entry_date= Label(win,text=geh[16])
              entry_date.grid(row=0,column=1)

              lbl_person_information=Label(win,text="Mitarbeiterinformation",pady=5)
              lbl_person_information.grid(row=1,column=0)

              lbl_fname=Label(win,text="First Name",pady=5)
              lbl_fname.grid(row=2,column=0)
              lbl_lname=Label(win,text="SurName",pady=5)
              lbl_lname.grid(row=2,column=1)
              lbl_birthdate=Label(win,text="Birthdate",pady=5)
              lbl_birthdate.grid(row=2,column=2)

              data_lname= Label(win,text=person[0][1])
              data_lname.grid(row=3,column=0)
              data_fname= Label(win,text=person[0][2])
              data_fname.grid(row=3,column=1)
              data_birthdate= Label(win,text=person[0][3])
              data_birthdate.grid(row=3,column=2)

              lbl_info=Label(win,text="Berufsinformation",pady=5)
              lbl_info.grid(row=4,column=0)
            
              lbl_brutto=Label(win,text="Brutto",pady=5)
              lbl_brutto.grid(row=5,column=0)
              lbl_stundensatz=Label(win,text="Stundensatz",pady=5)
              lbl_stundensatz.grid(row=5,column=1)
              lbl_monat=Label(win,text="Monat",pady=5)
              lbl_monat.grid(row=5,column=2)

              data_brutto= Label(win,text=loko[0][3])
              data_brutto.grid(row=6,column=0)
              data_stundensatz= Label(win,text=loko[0][4])
              data_stundensatz.grid(row=6,column=1)
              data_monat= Label(win,text=loko[0][5])
              data_monat.grid(row=6,column=2)

              lbl_geh=Label(win,text="Gehaltsabrechnung",pady=5)
              lbl_geh.grid(row=7,column=0)

              lbl_netto=Label(win,text="Der Nettolohn ",pady=5)
              lbl_netto.grid(row=8,column=0)
              data_netto= Label(win,text=geh[2])
              data_netto.grid(row=9,column=0)

              lbl_sv_bmg=Label(win,text="SV Bmg",pady=5)
              lbl_sv_bmg.grid(row=10,column=0)
              lbl_sv_lfd=Label(win,text="SV lfd")
              lbl_sv_lfd.grid(row=10,column=1)
              lbl_lst_bmg=Label(win,text="Lst Bmg")
              lbl_lst_bmg.grid(row=10,column=2)
              lbl_lohnsteuer=Label(win,text="Lohnsteuer",pady=5)
              lbl_lohnsteuer.grid(row=10,column=3)

              data_sv_bmg= Label(win,text=geh[3])
              data_sv_bmg.grid(row=11,column=0)
              data_sv_lfd= Label(win,text=geh[4])
              data_sv_lfd.grid(row=11,column=1)
              data_lst_bmg= Label(win,text=geh[5])
              data_lst_bmg.grid(row=11,column=2)
              data_lohnsteuer= Label(win,text=geh[6])
              data_lohnsteuer.grid(row=11,column=3)

              lbl_sobz=Label(win,text="Der sonstige Bezug(Netto)",pady=5)
              lbl_sobz.grid(row=12,column=0)
              data_sobz= Label(win,text=geh[7])
              data_sobz.grid(row=13,column=0)

              lbl_svsonder=Label(win,text="SV-Sonstiger Bezug",pady=5)
              lbl_svsonder.grid(row=14,column=0)
              lbl_lst_sb=Label(win,text="Lohnsteuer-Sonstiger Bezug",pady=5)
              lbl_lst_sb.grid(row=14,column=1)
              data_svsonder= Label(win,text=geh[8])
              data_svsonder.grid(row=15,column=0)
              data_lst_sb= Label(win,text=geh[9])
              data_lst_sb.grid(row=15,column=1)

              lbl_kommst=Label(win,text="Lohn/Kommunlasteuer",pady=5)
              lbl_kommst.grid(row=16,column=0)
              lbl_dga=Label(win,text="U-bahnsteuer",pady=5)
              lbl_dga.grid(row=16,column=1)
              lbl_db=Label(win,text="Dienstbeitrag",pady=5)
              lbl_db.grid(row=16,column=2)
              lbl_dz=Label(win,text="Zuschlag (DB)",pady=5)
              lbl_dz.grid(row=16,column=3)
              lbl_sv_dienstgeberbeitrag=Label(win,text="SV-Dienstgeberbeitrag",pady=5)
              lbl_sv_dienstgeberbeitrag.grid(row=16,column=4)
              lbl_bv=Label(win,text="BV",pady=5)
              lbl_bv.grid(row=16,column=5)
              data_kommst= Label(win,text=geh[10])
              data_kommst.grid(row=17,column=0)
              data_dga= Label(win,text=geh[11])
              data_dga.grid(row=17,column=1)
              data_db= Label(win,text=geh[12])
              data_db.grid(row=17,column=2)
              data_dz= Label(win,text=geh[13])
              data_dz.grid(row=17,column=3)
              data_sv_dienstgeberbeitrag= Label(win,text=geh[14])
              data_sv_dienstgeberbeitrag.grid(row=17,column=4)
              data_bv= Label(win,text=geh[15])
              data_bv.grid(row=17,column=5)
              ######################
              # end payroll window  #
              ######################
     
       # if geh not exist show message
       else:
              win=Toplevel(root)
              lbl=Label(win,text="Payrol not exist")
              lbl.grid(row=0,column=0)

# for the year chosen by the user, save the variable numbers in the formulas in database. 
def save_variable():
       # get information from tab4 form
       year=year_var.get()
       arb=entry_arb.get()
       bis=entry_bis.get()
       bis2=entry_bis2.get()
       uber=entry_über.get()
       son=entry_son.get()
       alg0=entry_allg0.get()
       alg=entry_allg.get()
       steuer=entry_steuer.get()
       alg42=entry_allg42.get()
       alg48=entry_allg48.get()
       alg50=entry_allg50.get()
       alg55=entry_allg55.get()
       fbp=entry_fbp.get()
       # save this data in database
       db.insert_variables(year,arb,bis,bis2,uber,son,alg0,alg,steuer,alg42,alg48,alg50,alg55,fbp)
       


       
              

       
  
root = Tk()
root.title("Tab Widget")

###############
# create tabs #
###############
tabControl = ttk.Notebook(root)
  
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)
tab3 = Frame(tabControl)
tab4 = Frame(tabControl)


# Employee registration tab
tabControl.add(tab1, text ='Mitarbeiterregistrierung')
# Create accounttab
tabControl.add(tab2, text ='Benutzerkonto erstellen')
# submit information tab
tabControl.add(tab3, text ='Informationen übermitteln')
# Payroll tab
tabControl.add(tab4, text ='Variablen')
tabControl.pack(expand = 1, fill ="both")
###################
# end create tabs #
###################

#############################
# Employee registration tab  #
#############################
# create a frame for logo image
frame = Frame(tab1, width=600, height=100)
frame.grid(row=0,column=0)
# put image in frame   
canvas = Canvas(frame, width = 600, height = 100)      
canvas.place(x=300,y=0)      
img = PhotoImage(file="logo.png")      
canvas.create_image(20,20, anchor=NW, image=img)      
# create a frame for form fields
frame2=Frame(tab1)
frame2.grid(row=1,column=0)
lbl_fname= Label(frame2, text="FirstName",pady=10)
lbl_fname.grid(row=1, column=0)
entry_fname = Entry(frame2)
entry_fname.grid(row=1, column=1)

lbl_lname= Label(frame2, text="Surnam",pady=10)
lbl_lname.grid(row=2, column=0)
entry_lname = Entry(frame2)
entry_lname.grid(row=2, column=1)

lbl_birthdate = Label(frame2, text="Geburtsdatum",pady=10)
lbl_birthdate.grid(row=3, column=0)
# calender
cal = DateEntry(frame2,pady=10)
 
cal.grid(row=3, column=1)
# Register Button 
register_btn=Button(frame2, text = "Registrieren",
       command = register_person,bg="#99ff33")
register_btn.grid(row=4, column=1)
# Cancel Button
cancel_btn=Button(frame2, text = "Stornieren",
       command =root.destroy,bg="#99ff33")
cancel_btn.grid(row=4, column=2)

##################################
# End Employee registration tab   #
##################################

######################
# Create account tab  #
######################

frame_tab2 = Frame(tab2, width=600, height=100)
frame_tab2.grid(row=0,column=0)
canvas2 = Canvas(frame_tab2, width = 600, height = 100)      
canvas2.place(x=300,y=0)      
img2 = PhotoImage(file="logo.png")      
canvas2.create_image(20,20, anchor=NW, image=img2)      
 
f2=Frame(tab2)
f2.grid(row=1,column=0)

# Employee name label
lbl_person_combo = Label(f2, text="Mitarbeitername",pady=10)
lbl_person_combo.grid(row=0, column=0)

# Create the list of options
person_list = db.select_all_persons()
if len(person_list) == 0:
       person_list.append("")  
# Variable to keep track of the option
# selected in OptionMenu
person_var = StringVar(root)
  
# Set the default value of the variable
person_var.set("Wähle eine Option")
  
# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
person_combo= OptionMenu(f2, person_var, *person_list)
person_combo.grid(row=0,column=1)

lbl_brutto = Label(f2,text="BRUTTO",pady=10)
lbl_brutto.grid(row=1,column=0)
entry_brutto = Entry(f2)
entry_brutto.grid(row=1, column=1)

lbl_stundensatz = Label(f2,text="Stundensatz",pady=10)
lbl_stundensatz.grid(row=2,column=0)
entry_stundensatz = Entry(f2)
entry_stundensatz.grid(row=2, column=1)

lbl_monat = Label(f2,text="Monat",pady=10)
lbl_monat.grid(row=3,column=0)
entry_monat = Entry(f2)
entry_monat.grid(row=3, column=1)

# Register Button 
register_btn2=Button(f2, text = "Registrieren", command=register_loko,bg="#99ff33")
register_btn2.grid(row=4, column=1)
# Cancel Button
cancel_btn2=Button(f2, text = "Stornieren",
       command =root.destroy,bg="#99ff33")
cancel_btn2.grid(row=4, column=2)
##########################
# End Create account tab  #
##########################

####################
# Create INFO tab  #
####################
frame_tab3 = Frame(tab3, width=600, height=100)
frame_tab3.grid(row=0,column=0)
canvas3 = Canvas(frame_tab3, width = 600, height = 100)      
canvas3.place(x=250,y=0)      
img3 = PhotoImage(file="logo.png")      
canvas3.create_image(20,20, anchor=NW, image=img3)  

frame_search=Frame(tab3)
frame_search.grid(row=1,column=0)

lbl_cal_payrol=Label(frame_search,text="Ausgabetag",pady=10 )
lbl_cal_payrol.grid(row=0, column=0)
cal_payrol = DateEntry(frame_search,pady=20)
cal_payrol.grid(row=0, column=1)

lbl_person_combo = Label(frame_search, text="Mitarbeitername",pady=10)
lbl_person_combo.grid(row=0, column=2)

# Create the list of options
loko_list = db.select_all_loko()
if len(loko_list) == 0:
       loko_list.append("")  
  
# Variable to keep track of the option
# selected in OptionMenu
loko_var = StringVar(root)
  
# Set the default value of the variable
loko_var.set("Wähle eine Option")
  
# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
person_combo= OptionMenu(frame_search, loko_var, *loko_list)
person_combo.grid(row=0,column=3)


f3=Frame(tab3)
f3.grid(row=2,column=0)
lbl_year = Label(f3, text="year",pady=10)
lbl_year.grid(row=0, column=0)

# Create the list of options
year_option = ["2022","2023","2024","2025","2026","2027","2028","2029","2030"] 
# Variable to keep track of the option
# selected in OptionMenu
year_option_var = StringVar(root)  
# Set the default value of the variable
year_option_var.set("2022")
  
# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
year_option_box= OptionMenu(f3, year_option_var, *year_option)
year_option_box.grid(row=0,column=1)

lbl_mehr0 = Label(f3,text="Mehrstunden mit 0%",pady=10,padx=30)
lbl_mehr0.grid(row=0,column=2)
entry_mehr0 = Entry(f3)
entry_mehr0.grid(row=0, column=3)

lbl_mehr25 = Label(f3,text="Mehrstunden mit 25%",pady=10)
lbl_mehr25.grid(row=1,column=0)
entry_mehr25 = Entry(f3)
entry_mehr25.grid(row=1, column=1)

lbl_mehr50 = Label(f3,text="Mehrstunden mit 50%",pady=10)
lbl_mehr50.grid(row=1,column=2)
entry_mehr50 = Entry(f3)
entry_mehr50.grid(row=1, column=3)

lbl_uberst50 = Label(f3,text="Überstunden mit 50% ",pady=10)
lbl_uberst50.grid(row=2,column=0)
entry_uberst50 = Entry(f3)
entry_uberst50.grid(row=2, column=1)

lbl_uberst100 = Label(f3,text="Überstunden mit 100%",pady=10)
lbl_uberst100.grid(row=2,column=2)
entry_uberst100 = Entry(f3)
entry_uberst100.grid(row=2, column=3)

lbl_sonderz = Label(f3,text="Sonderz",pady=10)
lbl_sonderz.grid(row=3,column=0)
entry_sonderz = Entry(f3)
entry_sonderz.grid(row=3, column=1)
entry_sonderz.bind_all("<Key>", on_key_press_sonderz)

lbl_altesonder = Label(f3,text="Brutto der Sonderzahlungen\n(des bisherigen Jahres)",pady=10)
lbl_altesonder.grid(row=3,column=2)
entry_altesonder = Entry(f3)
entry_altesonder.grid(row=3, column=3)
entry_altesonder.config(state= "disabled")
lbl_altesonder.config(state= "disabled")

lbl_diaten = Label(f3,text="Diaten",pady=10)
lbl_diaten.grid(row=4,column=0)
entry_diaten = Entry(f3)
entry_diaten.grid(row=4, column=1)

lbl_reisek = Label(f3,text="Reisek",pady=10)
lbl_reisek.grid(row=4,column=2)
entry_reisek = Entry(f3)
entry_reisek.grid(row=4, column=3)

lbl_sachbez = Label(f3,text="Sachbez",pady=10)
lbl_sachbez.grid(row=5,column=0)
entry_sachbez = Entry(f3)
entry_sachbez.grid(row=5, column=1)

lbl_fbb = Label(f3,text="Freibetragsbescheid",pady=10)
lbl_fbb.grid(row=5,column=2)
entry_fbb = Entry(f3)
entry_fbb.grid(row=5, column=3)

lbl_pp = Label(f3,text="Pendlerpauschale",pady=10)
lbl_pp.grid(row=6,column=0)
entry_pp = Entry(f3)
entry_pp.grid(row=6, column=1)

lbl_PEur  = Label(f3,text="Pendlereuro",pady=10)
lbl_PEur .grid(row=6,column=2)
entry_PEur  = Entry(f3)
entry_PEur .grid(row=6, column=3)

lbl_av = Label(f3,text="AlleinVerdiener-/AlleinErzieheranspruch\n(Anzahl der Kinder)",pady=10)
lbl_av.grid(row=7,column=0)
entry_av = Entry(f3)
entry_av.grid(row=7, column=1)

lbl_FaBoP_str  = Label(f3,text="Anspruch auf den Familienbonus",pady=10)
lbl_FaBoP_str .grid(row=7,column=2)

options_list = ["Yes", "No"]

FaBoP_var=StringVar()
FaBoP_var.set("Wähle eine Option")

FaBoP_str_combo= OptionMenu(f3,FaBoP_var, *options_list,command=FaBoP_str_combo_selected)
FaBoP_str_combo.grid(row=7,column=3)
 
lbl_u18g = Label(f3,text="Kinder unter 18 mit\nganzem Anspruch",pady=10)
lbl_u18g.grid(row=8,column=0)
entry_u18g = Entry(f3)
entry_u18g.grid(row=8, column=1)
entry_u18g.config(state="disabled")
lbl_u18g.config(state="disabled")

lbl_u18h = Label(f3,text="Kinder unter 18 mit\n halbem Anspruch",pady=10)
lbl_u18h.grid(row=8,column=2)
entry_u18h = Entry(f3)
entry_u18h.grid(row=8, column=3)
entry_u18h.config(state="disabled")
lbl_u18h.config(state="disabled")
# 
lbl_u_18g = Label(f3,text="Kinder über 18 mit\nganzem Anspruch",pady=10)
lbl_u_18g.grid(row=9,column=0)
entry_u_18g = Entry(f3)
entry_u_18g.grid(row=9, column=1)
entry_u_18g.config(state="disabled")
lbl_u_18g.config(state="disabled")

lbl_u_18h = Label(f3,text="Kinder über 18 mit\nhalbem Anspruch",pady=10)
lbl_u_18h.grid(row=9,column=2)
entry_u_18h = Entry(f3)
entry_u_18h.grid(row=9, column=3)
entry_u_18h.config(state="disabled")
lbl_u_18h.config(state="disabled")


lbl_ogb  = Label(f3,text="Arbeiter/Angestellte Gewerkschaftsmitglied",pady=10)
lbl_ogb .grid(row=10,column=0)

ogb_list = ["Yes", "No"]

ogb_var=StringVar()
ogb_var.set("Wähle eine Option")

ogb_str_combo= OptionMenu(f3,ogb_var, *ogb_list)
ogb_str_combo.grid(row=10,column=1)

lbl_j6 = Label(f3,text="aktuelle Jahressechstel (J/6)",pady=10)
lbl_j6.grid(row=10,column=2)
entry_j6 = Entry(f3)
entry_j6.grid(row=10, column=3)
entry_j6.config(state="disabled")
lbl_j6.config(state="disabled")


# Register Button 
register_btn3=Button(f3, text = "Registrieren",command=registe_info,bg="#99ff33")
register_btn3.grid(row=11, column=0)
# show payrol
payrol_btn3=Button(f3, text = "Gehaltsabrechnung",command=show_payrol,bg="#99ff33")
payrol_btn3.grid(row=11, column=1)
# Cancel Button
cancel_btn3=Button(f3, text = "Stornieren",
       command =root.destroy,bg="#99ff33")
cancel_btn3.grid(row=11, column=2)

####################
# End INFO tab      #
####################

####################
# Variablen tab     #
####################

frame_tab4 = Frame(tab4, width=600, height=100)
frame_tab4.grid(row=0,column=0)
canvas4 = Canvas(frame_tab4, width = 600, height = 100)      
canvas4.place(x=250,y=0)      
img4 = PhotoImage(file="logo.png")      
canvas4.create_image(20,20, anchor=NW, image=img4)      
 
f4=Frame(tab4)
f4.grid(row=1,column=0)

lbl_year = Label(f4, text="year",pady=10)
lbl_year.grid(row=0, column=0)

# Create the list of options
year_list = ["2022","2023","2024","2025","2026","2027","2028","2029","2030"] 
# Variable to keep track of the option
# selected in OptionMenu
year_var = StringVar(root)  
# Set the default value of the variable
year_var.set("Wähle eine Option")
  
# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
year_combo= OptionMenu(f4, year_var, *year_list)
year_combo.grid(row=0,column=1)

lbl_arb = Label(f4,text="arbeitlosenversicherung  bis",pady=10,padx=30)
lbl_arb.grid(row=1,column=0)
entry_arb = Entry(f4)
entry_arb.grid(row=1, column=1)
lbl_arb2 = Label(f4,text="0%",pady=10,padx=30)
lbl_arb2.grid(row=1,column=2)

lbl_bis = Label(f4,text="bis",pady=10,padx=30)
lbl_bis.grid(row=2,column=0)
entry_bis = Entry(f4)
entry_bis.grid(row=2, column=1)
lbl_bis2 = Label(f4,text="1%",pady=10,padx=30)
lbl_bis2.grid(row=2,column=2)

lbl_bis2 = Label(f4,text="bis",pady=10,padx=30)
lbl_bis2.grid(row=3,column=0)
entry_bis2 = Entry(f4)
entry_bis2.grid(row=3, column=1)
lbl_bis22 = Label(f4,text="2%",pady=10,padx=30)
lbl_bis22.grid(row=3,column=2)

lbl_über = Label(f4,text="über",pady=10,padx=30)
lbl_über.grid(row=4,column=0)
entry_über = Entry(f4)
entry_über.grid(row=4, column=1)
lbl_über = Label(f4,text="3%",pady=10,padx=30)
lbl_über.grid(row=4,column=2)

lbl_son = Label(f4,text="Sonderzahlung Jährlich",pady=10,padx=30)
lbl_son.grid(row=5,column=0)
entry_son = Entry(f4)
entry_son.grid(row=5, column=1)

lbl_allg0 = Label(f4,text="allg.Abzug ",pady=10,padx=30)
lbl_allg0.grid(row=6,column=0)
entry_allg0 = Entry(f4)
entry_allg0.grid(row=6, column=1)
lbl_allg02 = Label(f4,text="0%",pady=10,padx=30)
lbl_allg02.grid(row=6,column=2)

lbl_allg = Label(f4,text="allg.Abzug",pady=10,padx=30)
lbl_allg.grid(row=7,column=0)
entry_allg = Entry(f4)
entry_allg.grid(row=7, column=1)
lbl_steuer = Label(f4,text="steuer-staz",pady=10,padx=30)
lbl_steuer.grid(row=7,column=2)
entry_steuer = Entry(f4)
entry_steuer.grid(row=7, column=3)
lbl_steuer2 = Label(f4,text="%",pady=10,padx=30)
lbl_steuer2.grid(row=7,column=4)

lbl_allg42 = Label(f4,text="allg.Abzug ",pady=10,padx=30)
lbl_allg42.grid(row=8,column=0)
entry_allg42 = Entry(f4)
entry_allg42.grid(row=8, column=1)
lbl_allg422 = Label(f4,text="42%",pady=10,padx=30)
lbl_allg422.grid(row=8,column=2)

lbl_allg48 = Label(f4,text="allg.Abzug ",pady=10,padx=30)
lbl_allg48.grid(row=9,column=0)
entry_allg48 = Entry(f4)
entry_allg48.grid(row=9, column=1)
lbl_allg482 = Label(f4,text="48%",pady=10,padx=30)
lbl_allg482.grid(row=9,column=2)

lbl_allg50 = Label(f4,text="allg.Abzug ",pady=10,padx=30)
lbl_allg50.grid(row=10,column=0)
entry_allg50 = Entry(f4)
entry_allg50.grid(row=10, column=1)
lbl_allg502 = Label(f4,text="50%",pady=10,padx=30)
lbl_allg502.grid(row=10,column=2)

lbl_allg55 = Label(f4,text="allg.Abzu ",pady=10,padx=30)
lbl_allg55.grid(row=11,column=0)
entry_allg55 = Entry(f4)
entry_allg55.grid(row=11, column=1)
lbl_allg552 = Label(f4,text="55%",pady=10,padx=30)
lbl_allg552.grid(row=11,column=2)

lbl_fbp = Label(f4,text="Failienbonus Plus ",pady=10,padx=30)
lbl_fbp.grid(row=12,column=0)
entry_fbp = Entry(f4)
entry_fbp.grid(row=12,column=1)

# Register Button 
register_btn2=Button(f4, text = "Registrieren", command=save_variable,bg="#99ff33")
register_btn2.grid(row=13, column=1)
# Cancel Button
cancel_btn2=Button(f4, text = "Stornieren",
       command =root.destroy,bg="#99ff33")
cancel_btn2.grid(row=13, column=2)
####################
# End Variablen tab     #
####################
root.mainloop()  