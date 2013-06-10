from bottle import route, run, template, response, request, redirect
from main import auth, conn, hoitajat
from sqlite3 import IntegrityError

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
    
    try:
        auth.login(name, password)
    except:
        return template("loginForm", viesti = "Sisäänkirjautuminen epäonnistui")
    redirect("/")

@route("/logout")
def logout():
    auth.logout()
    return template("logout")

@route("/register")
def register_get():
    return template("register", viesti = None)

@route("/register", method="POST")
def register_post():
    name = request.forms.get("name")
    password1 = request.forms.get("password1")
    password2 = request.forms.get("password2")
    
    if password1 != password2:
        return template("register", viesti = "Salasanat eivät täsmää")
    try:
        auth.register(name, password1)
    except IntegrityError:
        return template("register", viesti = "Valitsemasi käyttäjätunnus on jo käytössä")
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
    
@route("/hallinta")
def hallinta():
    return template("hallinta")

@route("/hoitajat")
def hoitajat_get():
    hoitsut = hoitajat.kaikkiHoitajat()
    return template("hoitajat", hoita =hoitsut)
    
@route("/hoitajat", method="POST")
def hoitajat_post():
    nimi = request.forms.get("nimi")
    luvat = request.forms.get("luvat")
    hoitajat.uusi(nimi, luvat.split(","))
    redirect("/hoitajat")
    
    
@route("/asiakkaat")
def asiakkaat():
    return template("asiakkaat")
    
@route("/hoitovuorot")
def hoitovuorot():
    testiarvot = {"Milla-hoitsu":["Kiiranen", "Loppi", "Aatos", "Mölläs"], "Kalle-hoitsu":["Kärttynen", "Kolho", "Pieniniemi"]}
    return template("hoitovuorot", hoitajat = testiarvot)
