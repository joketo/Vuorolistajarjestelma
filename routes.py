from bottle import route, run, template, response, request, redirect
from main import auth, conn

#testisyötettä formeille
def rand():
    return random.choice([True,False])

@route("/")
def etusivu():
    if not auth.isLogged():
        redirect("/login")
    return template("front")

@route("/login")
def login_form():
    return template("loginForm", viesti = None)

@route("/login", method="POST")
def login_submit():
    name = request.forms.get("name")
    password = request.forms.get("password")

    success = auth.login(name, password)
    if not success:
        return template("loginForm", viesti = "Sisäänkirjautuminen epäonnistui")
    redirect("/")

@route("/logout")
def logout():
    auth.logout()
    return template("logout")

@route("/register")
def register_form():
    return template("register")

@route("/register", method="POST")
def register():
    name = request.forms.get("name")
    password = request.forms.get("password")
    
    auth.register(name, password)
    return template("rekOK")

@route("/whoami")
def whoami():
    islogged = auth.isLogged()
    name = auth.loggedAs()
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
