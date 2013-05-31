from bottle import route, run, template, response, request
from beaker.middleware import SessionMiddleware
import bottle
import auth
import random
import sqlite3

from sqlite_backend import Users

conn = sqlite3.connect("test.db")


session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': Truek
}
app = SessionMiddleware(bottle.app(), session_opts)

a = auth.Auth(Users("test.db"))
def rand():
    return random.choice([True,False])

@route("/")
def etusivu():
    return template("front")

@route("/login")
def login_form():
    return template("loginForm")

@route("/login", method="POST")
def login_submit():
    name = request.forms.get("name")
    password = request.forms.get("password")

    success = a.login(name, password)
    return template("loginSubmit", success=success)
        

@route("/logout")
def logout():
    a.logout()
    return template("logout")

@route("/register")
def register_form():
    return template("register")

@route("/register", method="POST")
def register():
    name = request.forms.get("name")
    password = request.forms.get("password")
    
    a.register(name, password)
    return "Registration complete"

@route("/whoami")
def whoami():
    islogged = a.isLogged()
    name = a.loggedAs()
    return template("whoAmI", islogged=islogged, name=name)


@route("/registered")
def registered():
    c = conn.cursor()
    c.execute("SELECT id, username from users")
    users = c.fetchall()
    return template("registered", users = str(users))

@route("/test")
def test():
    return template("test", nimet=["a", "b", "c"], rand=rand)

@route("/possibleCustomers")
def asiakkaat():
    return template("possibleCustomers", hoitajat =["a", "b"], potilaat =["i", "j", "k", "h"], rand=rand)

if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)

