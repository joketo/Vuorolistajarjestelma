import os
import sys
import bottle
import sqlite3
from beaker.middleware import SessionMiddleware

import routes
import create_tables
from sqlite_backend import Hoitajat, Asiakkaat, Users
from auth import Auth


dbfile = "test.db" if len(sys.argv)<2 else sys.argv[1]

#onko tietokanta olemassa? jos ei, luo se
if not os.path.isfile(dbfile):
    create_tables.create_all(dbfile)
    

#tietokantayhteys ja backend-oliot
conn = sqlite3.connect(dbfile)
hoitajat = Hoitajat(conn)
asiakkaat = Asiakkaat(conn)
auth = Auth(Users(conn))

# beaker-asetukset
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 2000,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

if __name__ == "__main__":
    conn.execute("PRAGMA synchronous=OFF")
    bottle.run(app=app, host='localhost', port=8080, debug=True, reloader=True)
    bottle.app()

