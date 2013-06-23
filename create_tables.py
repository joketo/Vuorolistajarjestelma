"""
Skripta tyhjän tietokannan luomiseen, tätä voi käyttää stand-alonena
tai kutsua muusta koodista (main.py kutsuu tätä jos tietokantaa ei ole)
"""

import sqlite3
import sys
import os


def usedb(dbname, dbstring, createparams=tuple()):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(dbstring, createparams)
    conn.commit()
    conn.close()

def create_users(dbname):
    usedb(dbname, """CREATE TABLE users
                    (id integer primary key autoincrement,
                     username text unique not null, 
                     salt blob, hash blob)""")


def create_hoitajat(dbname):
    usedb(dbname, """CREATE TABLE hoitajat
                     (id integer primary key autoincrement,
                      nimi text unique not null)""")


def create_asiakkaat(dbname):
    usedb(dbname, """CREATE TABLE asiakkaat
                     (id integer primary key autoincrement,
                      nimi text unique not null)""")


def create_kaynnit(dbname):
    usedb(dbname, """CREATE TABLE kaynnit
                     (id integer primary key autoincrement,
                      asiakasid integer references asiakkaat(id) on delete cascade,
                      paivaid integer references paivat(id) on delete cascade,
                      aikaid integer references ajat(id) on delete cascade,
                      kestoid integer not null)
                   """)


def create_kayntiluvat(dbname):
    usedb(dbname, """Create TABLE kayntiluvat
                     (kayntiid integer references kaynnit(id) on delete cascade, 
                     lupaid integer references luvat(id) on delete cascade)
                   """)


def create_hoitajaluvat(dbname):
    usedb(dbname, """CREATE TABLE hoitajaluvat
                     (hoitajaid integer references hoitajat(id) on delete cascade,
                     lupaid integer references luvat(id) on delete cascade)
                  """)


def create_luvat(dbname):
    """Luo taulun mahdollisista luvista"""
    usedb(dbname, """CREATE TABLE luvat
                     (id integer primary key autoincrement,
                      lupa text unique not null)""")
    luvat = ["lääke", "haavat", "silmätipat", "piikit"]
    for lupa in luvat:
        usedb(dbname, """INSERT INTO luvat (lupa)
                         VALUES (?)""", (lupa,))


def create_paivat(dbname):
    """Luo taulun joka sisältää päivien nimet"""
    usedb(dbname, """CREATE TABLE paivat
                     (id integer primary key autoincrement,
                      paiva text unique not null)""")
                      
    paivat = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    for paiva in paivat:
        usedb(dbname, """INSERT INTO paivat (paiva)
                         VALUES (?)""", (paiva,))
                         

def create_ajat(dbname):
    """Luo taulukon valideista aikaväleistä"""
    usedb(dbname, """CREATE TABLE ajat
                     (id integer primary key autoincrement,
                      aika text unique not null)""")
     
    ajat = ["8-10", "10-12", "12-14", "16-20", "20-22"]
    for aika in ajat:
        usedb(dbname, """INSERT INTO ajat (aika)
                         VALUES (?)""", (aika,))


def create_kestot(dbname):
    """Luo taulukon sallituista käyntien kestoista"""
    usedb(dbname, """CREATE TABLE kestot
                     (id integer primary key autoincrement,
                      kesto integer unique not null)""")
                      
    kestot = [10, 15, 20, 30, 45, 50, 60]
    for kesto in kestot:
        usedb(dbname, """INSERT INTO kestot (kesto)
                         VALUES (?)""", (kesto,))


def create_all(db):
    create_users(db)
    create_hoitajat(db)
    create_asiakkaat(db)
    create_kaynnit(db)
    create_kayntiluvat(db)
    create_hoitajaluvat(db)
    create_luvat(db)
    create_paivat(db)
    create_ajat(db)
    create_kestot(db)

if __name__ == '__main__':
    dbname = "test.db" if len(sys.argv)<2 else sys.argv[1]
    try:
        create_all(dbname)
    except Exception:
        # luotiin luultavasti rikkinäinen tietokanta, poistetaan se
        os.remove(dbname)
