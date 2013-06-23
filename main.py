import os
import sys
import argparse
import bottle
import sqlite3
from beaker.middleware import SessionMiddleware

import routes
import create_tables
from sqlite_backend import Hoitajat, Asiakkaat, Users
from auth import Auth


if __name__ == '__main__':
    # hae komentoriviparametrit argparsella
    # TODO: väännä argparsen helppi suomeksi
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", type=str, help="Tietokantatiedosto", default="test.db")
    parser.add_argument("--nosync", "-n", help="Laita sqliten synkronointi pois. Vaarallinen mutta paljon nopeampi esim. nfs-jaolta ajaessa", action="store_true")
    args = parser.parse_args()
    #onko tietokanta olemassa? jos ei, luo se
    if not os.path.isfile(args.db):
        create_tables.create_all(args.db)

    #tietokantayhteys ja backend-oliot
    conn = sqlite3.connect(args.db)
    hoitajat = Hoitajat(conn)
    asiakkaat = Asiakkaat(conn)
    auth = Auth(Users(conn))
    
    if args.nosync:
        conn.execute("PRAGMA synchronous=OFF")

    # beaker-asetukset
    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': 2000,
        'session.auto': True
    }
    app = SessionMiddleware(bottle.app(), session_opts)
    app.app.hoitajat = hoitajat
    app.app.asiakkaat = asiakkaat
    app.app.auth = auth
    # päräytä itse ohjelma käyntiin
    bottle.run(app=app, host='localhost', port=8080, debug=True, reloader=True)


