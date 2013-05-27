from bottle import route, run, template, response, request
from beaker.middleware import SessionMiddleware
import bottle
import auth
import random

session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

a = auth.Auth()
def rand():
    return random.choice([True,False])

@route("/")
def etusivu():
    return template("front")

@route("/login")
def login_form():
    return template("login")

@route("/login", method="POST")
def login_submit():
    name = request.forms.get("name")
    password = request.forms.get("password")

    if a.login(name, password):
        return "Logged in!"
    else:
        return "Login failed"

@route("/logout")
def logout():
    a.logout()

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
    if a.isLogged():
        return template("""You are logged in as {{name}}""", name=a.loggedAs())
    else: return """You are not logged in"""

@route("/registered")
def registered():
    return str(a.users)

@route("/test")
def test():
    return template("test", nimet=["a", "b", "c"], rand=rand)

@route("/possibleCustomers")
def asiakkaat():
    return template("possibleCustomers", hoitajat =["a", "b"], potilaat =["i", "j", "k", "h"], rand=rand)

if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)

