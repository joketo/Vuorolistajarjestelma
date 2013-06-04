import sqlite3


def usedb(dbname, dbstring, createparams=tuple()):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(dbstring, createparams)
    conn.commit()
    conn.close()

#TODO: sqlite lisää automaattisesti nopeasti hakevat rowid:t! turhat tauhkat pois...
def create_users(dbname):
    usedb(dbname,"""CREATE TABLE users
                    (id integer primary key autoincrement, username text unique not null, 
                     salt blob, hash blob)""")

def create_hoitsut(dbname):
    usedb(dbname, """CREATE TABLE hoitajat
                     (nimi text unique not null, luvat blob)""")

def create_kaynnit(dbname):
    usedb(dbname, """CREATE TABLE kaynnit
                     (asiakas text not null, vaatimukset blob, kesto text, hoitaja text)""")

def create_luvat(dbname):
    usedb(dbname, """CREATE TABLE luvat
                     (lupa text unique)""")

def create_hoitajaluvat(dbname):
    usedb(dbname, """CREATE TABLE hoitajaluvat
                     (hoitajaid integer, lupaid integer)""")

def create_asiakasluvat(dbname):
    usedb(dbname, """CREATE TABLE asiakasluvat
                     (asiakasid niteger, lupaid integer)""")

db = "test.db"
create_users(db)
create_hoitsut(db)
create_kaynnit(db)
create_luvat(db)
create_hoitajaluvat(db)
create_asiakasluvat(db)
