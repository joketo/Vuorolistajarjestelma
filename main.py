from bottle import route, run, template, response, request
from beaker.middleware import SessionMiddleware
import bottle
import random
import sqlite3

from sqlite_backend import Hoitajat

from auth import Auth
import routes

from sqlite_backend import Users

conn = sqlite3.connect("test.db")

hoitajat = Hoitajat(conn)

# beaker-asetukset
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 2000,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

auth = Auth(Users(conn))


if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)

