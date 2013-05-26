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
    name = request.get_cookie("name")
    sid = request.get_cookie("sid")
    a.logout(name, sid)
        

@route("/nah")
def nah():
    return """nope"""

@route("/whoami")
def whoami():
    name = request.get_cookie("name")
    sid = request.get_cookie("sid")

    print(name,sid)
    if a.isLogged(name, sid):
        return template("""You are logged in as {{name}}""", name=name)
    else: return """You are not logged in"""

@route("/test")
def test():
    return template("test", nimet=["a", "b", "c"], rand=rand)

@route("/possibleCustomers")
def asiakkaat():
    return template("possibleCustomers", hoitajat =["a", "b"], potilaat =["i", "j", "k", "h"], rand=rand)

if __name__ == "__main__":
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)

