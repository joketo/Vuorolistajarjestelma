import sqlite3

def create_tables():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE users
              (id integer primary key autoincrement, username text UNIQUE, 
              salt blob, hash blob)""")
    conn.commit()
    conn.close()

create_tables()
