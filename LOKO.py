import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"./LOKO.db"
    # table for save person information
    sql_create_PERS_table = """ CREATE TABLE IF NOT EXISTS PERS (
                                        PERS_ID integer PRIMARY KEY AUTOINCREMENT,
                                        PERS_SURNAME text NOT NULL,
                                        PERS_FIRSTNAME text NOT NULL,
                                        PERS_BIRTHDATE date NOT NULL
                                    ); """
    # create loko table
    # this table save person id To access the person to whom this account belongs.
    sql_create_LOKO_table = """CREATE TABLE IF NOT EXISTS LOKO (
                                    PERS_ID integer NOT NULL,
                                    LOKO_ID integer PRIMARY KEY AUTOINCREMENT,
                                    LOKO_DATE text NOT NULL,
                                    LOKO_BRUTTO float NOT NULL,
                                    LOKO_stundensatz float NOT NULL,
                                    LOKO_monat float NOT NULL,
                                    FOREIGN KEY (PERS_ID) REFERENCES PERS (PERS_ID)
                                );"""
    # this table save input information
    # this table save loko id To access the account
    sql_create_INFO_table = """CREATE TABLE IF NOT EXISTS INFO (
                                    LOKO_ID integer NOT NULL,
                                    INFO_ID integer PRIMARY KEY AUTOINCREMENT,
                                    INFO_mehr0 float NOT NULL,
                                    INFO_mehr25 float NOT NULL,
                                    INFO_mehr50 float NOT NULL,
                                    INFO_uberst50 float NOT NULL,
                                    INFO_uberst100 float NOT NULL,
                                    INFO_sonderz float NOT NULL,
                                    INFO_sachbez float NOT NULL,
                                    INFO_diaten float NOT NULL,
                                    INFO_reisek float NOT NULL,
                                    INFO_altesonder float,
                                    INFO_FBB float NOT NULL,
                                    INFO_PP float NOT NULL,
                                    INFO_PEur float NOT NULL,
                                    INFO_av integer,
                                    INFO_u18g integer,
                                    INFO_u18h integer,
                                    INFO_u_18g integer,
                                    INFO_u_18h integer,
                                    INFO_OGB text,
                                    INFO_j6 float,
                                    FOREIGN KEY (LOKO_ID) REFERENCES PERS (LOKO_ID)
                                );"""
    # This table stores the result of the calculations and the information displayed in the pay slip
    #  this table save loko id To access the account
    sql_create_GEH_table = """CREATE TABLE IF NOT EXISTS GEH (
                                    GEH_ID integer PRIMARY KEY AUTOINCREMENT,
                                    LOKO_ID integer NOT NULL,
                                    GEH_netto float NOT NULL,
                                    GEH_sv_bmg float NOT NULL,
                                    GEH_sv float NOT NULL,
                                    GEH_lst_bmg float NOT NULL,
                                    GEH_lst float NOT NULL,
                                    GEH_sobz float NOT NULL,
                                    GEH_svsonder float NOT NULL,
                                    GEH_lst_sb float NOT NULL,
                                    GEH_kommst float NOT NULL,
                                    GEH_dga float NOT NULL,
                                    GEH_db float NOT NULL,
                                    GEH_dz float NOT NULL,
                                    GEH_sv_dienstgeberbeitrag float NOT NULL,
                                    GEH_bv float NOT NULL,
                                    GEH_Date date,
                                    FOREIGN KEY (LOKO_ID) REFERENCES PERS (LOKO_ID)
                                );"""
    # table for save Numbers used in formulas.
    sql_create_VAR_table = """ CREATE TABLE IF NOT EXISTS VAR (
                                    VAR_ID integer PRIMARY KEY AUTOINCREMENT,
                                    VAR_year text NOT NULL,
                                    VAR_arb float NOT NULL,
                                    VAR_bis float NOT NULL,
                                    VAR_bis2 float NOT NULL,
                                    VAR_uber float NOT NULL,
                                    VAR_son float NOT NULL,
                                    VAR_alg0 float NOT NULL,
                                    VAR_alg float NOT NULL,
                                    VAR_steuer float NOT NULL,
                                    VAR_alg42 float NOT NULL,
                                    VAR_alg48 float NOT NULL,
                                    VAR_alg50 float NOT NULL,
                                    VAR_alg55 float NOT NULL,
                                    VAR_fbp float NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_PERS_table)

        # create tasks table
        create_table(conn, sql_create_LOKO_table)
        create_table(conn, sql_create_INFO_table)
        create_table(conn, sql_create_GEH_table)
        create_table(conn, sql_create_VAR_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()