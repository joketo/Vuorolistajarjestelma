import sqlite3
import sys

def usedb(dbname, dbstring, createparams=tuple()):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(dbstring, createparams)
    conn.commit()
    conn.close()

def create_users(dbname):
    usedb(dbname, """CREATE TABLE users
                    (id integer primary key autoincrement, username text unique not null, 
                     salt blob, hash blob)""")


def create_hoitsut(dbname):
    usedb(dbname, """CREATE TABLE hoitajat
                     (nimi text unique not null)""")


def create_asiakkaat(dbname):
    usedb(dbname, """CREATE TABLE asiakkaat
                     (nimi text unique not null)""")


def create_kaynnit(dbname):
    usedb(dbname, """CREATE TABLE kaynnit
                     (asiakasid integer not null,
                      paiva integer not null,
                      aika integer not null,
                      kesto integer not null)""")


def create_kayntiluvat(dbname):
    usedb(dbname, """Create TABLE kayntiluvat
                     (kayntiid integer, lupa text)""")


def create_hoitajaluvat(dbname):
    usedb(dbname, """CREATE TABLE hoitajaluvat
                     (hoitajaid integer, lupa text)""")

def create_all(db):
    create_users(db)
    create_hoitsut(db)
    create_asiakkaat(db)
    create_kaynnit(db)
    create_kayntiluvat(db)
    create_hoitajaluvat(db)

if __name__ == '__main__':
    dbname = "test.db" if len(sys.argv)<2 else sys.argv[1]
    create_all(dbname)

