import sqlite3
import datetime
#  This class performs database operations
# This class in its constructor function receives the name of a database and connects to it.
class Database():
    def __init__(self,db_name):
        self.db_name = db_name
        self.connect_to_db()
    # connect to database
    def connect_to_db(self):
        # The try block lets you test a block of code for errors. The except block lets you handle the error. The else block lets you execute code when there is no .
        try:
            # create connection
            self.sqliteConnection = sqlite3.connect(self.db_name)
            # create cursor
            # A database cursor is an identifier associated with a group of rows. It is, in a sense, a pointer to the current row in a buffer. 
            self.cursor = self.sqliteConnection.cursor()
        # if above code failed.execute this block           
        except sqlite3.Error as error:
            print("Failed to connect Database", error)
        finally:
            print("Successfully Connected to SQLite")
    
    def insert_person(self,surname, firstname, birthdate):
        try:
            # insert query for register data in PERS table
            # The input values are variable, so we put "?" instead
            sqlite_insert_query = """INSERT INTO PERS
                                (PERS_SURNAME, PERS_FIRSTNAME, PERS_BIRTHDATE) 
                                VALUES 
                                (?, ?, ?)"""
            # data tuple for replace in '?' character 
            data= (surname, firstname, birthdate)
            # excute above query
            count = self.cursor.execute(sqlite_insert_query,data)
            # We keep the ID of the person we just registered to enter it in other tables.
            self.person_id = self.cursor.lastrowid
            # aplay this changes to database
            self.sqliteConnection.commit()
            print("Record inserted successfully", self.cursor.rowcount)

        except sqlite3.Error as error:
            print("Failed to insert data", error)

    def insert_loko(self,person_id,monat,stundensatz,brutto):
        try:
            sqlite_insert_query = """INSERT INTO LOKO
                                (PERS_ID, LOKO_DATE, LOKO_BRUTTO, LOKO_stundensatz, LOKO_monat) 
                                VALUES 
                                (?,?,?,?,?)"""
            data= (person_id,str(datetime.datetime.now()),brutto,stundensatz,monat)

            count = self.cursor.execute(sqlite_insert_query,data)
            self.loko_id = self.cursor.lastrowid
            self.sqliteConnection.commit()
            print("Record inserted successfully", self.cursor.rowcount)
    

        except sqlite3.Error as error:
            print("Failed to insert data", error)
    
    def insert_information(self,loko_id,mehr0,mehr25,mehr50,überst50,überst100,sonderz,sachbez,diäten,reisek,FBB,PP,PEur,u18g,u18h,j6):
        try:
            sqlite_insert_query = """INSERT INTO INFo
                                (LOKO_ID, INFO_mehr0, INFO_mehr25, INFO_mehr50, INFO_uberst50,INFO_uberst100,INFO_sonderz,INFO_sachbez,INFO_diaten,INFO_reisek,INFO_FBB,INFO_PP,INFO_PEur,INFO_u18g,INFO_u18h,INFO_j6) 
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            data= (loko_id,mehr0,mehr25,mehr50,überst50,überst100,sonderz,sachbez,diäten,reisek,FBB,PP,PEur,u18g,u18h,j6)

            count = self.cursor.execute(sqlite_insert_query,data)
            self.sqliteConnection.commit()
            print("Record inserted successfully", self.cursor.rowcount)
        

        except sqlite3.Error as error:
            print("Failed to insert data", error)
    
    def insert_Gehaltsabrechnung(self,loko_id,netto,sv_bmg,sv, lst_bmg,lst,sobz,svsonder,lst_sb,kommst,dga,db,dz,sv_dienstgeberbeitrag,bv,date):
        try:
            sqlite_insert_query = """INSERT INTO GEH
                                (LOKO_ID,GEH_netto, GEH_sv_bmg, GEH_sv,GEH_lst_bmg,GEH_lst,GEH_sobz,GEH_svsonder,GEH_lst_sb,GEH_kommst,GEH_dga,GEH_db,GEH_dz,GEH_sv_dienstgeberbeitrag,GEH_bv,GEH_date) 
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            data= (loko_id,netto,sv_bmg,sv, lst_bmg,lst,sobz,svsonder,lst_sb,kommst,dga,db,dz,sv_dienstgeberbeitrag,bv,date)

            count = self.cursor.execute(sqlite_insert_query,data)
            self.sqliteConnection.commit()
            print("Record inserted successfully", self.cursor.rowcount)
            # destroy cursor
            self.cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data", error)
        finally:
            # destroy connection
            if self.sqliteConnection:
                self.sqliteConnection.close()
                print("The SQLite connection is closed")
    # fetch all data from PERS table
    def select_all_persons(self):
        # select query
        query = """SELECT * FROM PERS"""
        # execut query
        p=self.cursor.execute(query)
        # fetch all person from database.recieve it tuple format
        persons=p.fetchall()
        persons_name=[]
        for i in persons:
            # save person information in list
            persons_name.append(str(i[0])+"."+i[1]+" "+i[2])
        # return person list 
        return persons_name
    # In order to display the name and ID of the person's account in the option box, we must extract this information from the two tables PERS and LOKO. We do this with the JOIN command.
    def select_all_loko(self):
        query = """SELECT * FROM LOKO INNER JOIN PERS ON PERS.PERS_ID=LOKO.PERS_ID"""
        p=self.cursor.execute(query)
        persons=p.fetchall()
        # print(persons)
        persons_name=[]
        for i in persons:
            persons_name.append("Loko Id: "+str(i[1])+" Name: "+i[7]+" "+i[8])
        return persons_name
        # print(persons_name)
    # select loko information from database based on id
    def select_loko_with_id(self,id):
        # when excute this query replaced %s with id
        query = "SELECT * FROM LOKO WHERE PERS_ID=%s"%(id)
        l=self.cursor.execute(query)
        loko=l.fetchall()
        return loko
    def select_person_with_id(self,id):
        query = "SELECT * FROM PERS WHERE PERS_ID=%s"%(id)
        p=self.cursor.execute(query)
        person=p.fetchall()
        return person
    def select_geh(self,loko_id,date):
        query = "SELECT * FROM GEH WHERE LOKO_ID=%s AND GEH_date='%s'"%(loko_id, date)
        # print(query)
        g=self.cursor.execute(query)
        geh=g.fetchall()
        return geh
    
    def insert_variables(self,year,arb,bis,bis2,uber,son,alg0,alg,steuer,alg42,alg48,alg50,alg55,fbp):
        try:
            sqlite_insert_query = """INSERT INTO VAR
                                (VAR_year,VAR_arb,VAR_bis,VAR_bis2,VAR_uber,VAR_son,VAR_alg0,VAR_alg,VAR_steuer,VAR_alg42,VAR_alg48,VAR_alg50,VAR_alg55,VAR_fbp) 
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            data= (year,arb,bis,bis2,uber,son,alg0,alg,steuer,alg42,alg48,alg50,alg55,fbp)

            count = self.cursor.execute(sqlite_insert_query,data)
            self.sqliteConnection.commit()
            print("Record inserted successfully", self.cursor.rowcount)
    
        except sqlite3.Error as error:
            print("Failed to insert data", error)

    def select_variables_based_year(self,year):
        query = "SELECT * FROM VAR WHERE VAR_year=%s"%(year)
        y=self.cursor.execute(query)
        variables=y.fetchall()
        print(variables)
        return variables






# d=Database('LOKO.db')
# d.select_variables_based_year("2022")


    

    
