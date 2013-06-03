import sqlite3

def usedb(dbname, dbstring, createparams=tuple()):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(requeststring, createparams)
    conn.commit()
    conn.close()

def create_users(dbname):
    accessdb("""CREATE TABLE users
                (id integer primary key autoincrement, username text UNIQUE, 
                 salt blob, hash blob)""")

def create_hoitsut(dbname):
    usedb("""Create TABLE hoitajat
             (id integer primary key autoincrement, name text UNIQUE,
              perms blob)""")

create_users("test.db")
create_hoitsut("test.db")
