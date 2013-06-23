import os
import argparse
import bottle
import sqlite3
from beaker.middleware import SessionMiddleware

import routes
import create_tables
from sqlite_backend import Hoitajat, Asiakkaat, Users, Vakiot
from auth import Auth


if __name__ == '__main__':
    # hae komentoriviparametrit argparsella
    # TODO: väännä argparsen helppi suomeksi
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", type=str, help="Tietokantatiedosto", default="test.db")
    parser.add_argument("--nosync", "-n", help="Laita sqliten synkronointi pois."
                                               + "Vaarallinen mutta paljon nopeampi esim. nfs-jaolta" +
                                               " ajaessa", action="store_true")
    args = parser.parse_args()
    #onko tietokanta olemassa? jos ei, luo se
    if not os.path.isfile(args.db):
        create_tables.create_all(args.db)

    #tietokantayhteys ja backend-oliot
    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")
    hoitajat = Hoitajat(conn)
    asiakkaat = Asiakkaat(conn)
    auth = Auth(Users(conn))
    vakiot = Vakiot(conn)
    
    if args.nosync:
        conn.execute("PRAGMA synchronous=OFF")

    # beaker-asetukset
    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': 2000,
        'session.auto': True
    }
    
    app = SessionMiddleware(bottle.app(), session_opts)

    # tietokantaoliot käytettäviksi muulle ohjelmalle
    # oliot löytyvät nyt Bottle.app().hoitajat jne.
    app.app.hoitajat = hoitajat
    app.app.asiakkaat = asiakkaat
    app.app.auth = auth
    app.app.vakiot = vakiot

    # päräytä itse ohjelma käyntiin
    bottle.run(app=app, host='localhost', port=8080, debug=True, reloader=True)


