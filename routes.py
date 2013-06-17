from bottle import route, run, template, response, request, redirect, static_file
from main import auth, conn, hoitajat, asiakkaat
from sqlite3 import IntegrityError
import vakioita


def loginVaaditaan():
    if not auth.isLogged():
        redirect("/login")
    

@route("/")
def etusivu():
    loginVaaditaan()
    return template("front")


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@route("/login")
def login_form():
    return template("loginForm", viesti=None)


@route("/login", method="POST")
def login_submit():
    name = request.forms.getunicode("name")
    password = request.forms.getunicode("password")
    
    try:
        auth.login(name, password)
    # Innokas except jottei loginin epäonnistumisviesti anna vihjeitä hyökkääjälle
    except:
        return template("loginForm", viesti="Sisäänkirjautuminen epäonnistui")
    redirect("/")


@route("/logout")
def logout():
    auth.logout()
    return template("logout")


@route("/register")
def register_get():
    return template("register", viesti=None)


@route("/register", method="POST")
def register_post():
    name = request.forms.getunicode("name")
    password1 = request.forms.getunicode("password1")
    password2 = request.forms.getunicode("password2")
    
    if password1 != password2:
        return template("register", viesti="Salasanat eivät täsmää")
    try:
        auth.register(name, password1)
    except IntegrityError:
        return template("register", viesti="Valitsemasi käyttäjätunnus on jo käytössä")
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
    return template("registered", users=str(users))


@route("/hoitajat")
def hoitajat_get():
    loginVaaditaan()
    hoitsut = hoitajat.kaikki()
    return template("hoitajat", hoitajat=hoitsut)
    

@route("/hoitajat", method="POST")
def hoitajat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    luvat = request.forms.getall("lupa")
    # kai tähän pitää olla fiksumpi tapa, ei ole getallunicode()-metodia...
    luvat = [l.encode("latin-1").decode("utf8") for l in luvat]
    hoitajat.uusi(nimi, luvat)
    print(type(nimi), nimi, luvat)
    redirect("/hoitajat")



@route("/asiakkaat", method="POST")
def asiakkaat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    asiakkaat.uusi(nimi)
    redirect("/asiakkaanHallinta")
    
    
@route("/asiakkaanHallinta")
def asiakkaanHallinta():
    loginVaaditaan()
    return template("asiakkaanHallinta", asiakkaat=asiakkaat.kaikki())
    
    

@route("/lisaaVuoro", method="POST")
def lisaaVuoro_post():
    loginVaaditaan()
    request.forms.recode_unicode = True
    asiakasid = request.forms.getunicode("asiakas")
    paiva = request.forms.getunicode("paiva")
    aika = request.forms.getunicode("aika")
    kesto = request.forms.getunicode("kesto")
    luvat = request.forms.getall("lupa")
    # kai tähän pitää olla fiksumpi tapa, ei ole getallunicode()-metodia...
    luvat = [l.encode("latin-1").decode("utf8") for l in luvat]
    asiakkaat.lisaaKaynti(asiakasid, kesto, aika, paiva, luvat)
    redirect("/asiakkaanHallinta")


@route("/hoitovuorot")
def hoitovuorot():
    # TODO: luo hoitovuorot jossain muualla
    # jakaa hoitovuoron mahdollisista hoitajista aina sille, jolla on
    # vähiten käyntejä
    hoitokerrat = {h: 0 for h in map(lambda h: h.nimi, hoitajat.kaikki())}
    hoitovuorot = {h: [] for h in map(lambda h: h.nimi, hoitajat.kaikki())}
    for k in asiakkaat.kaikkiKaynnit():
        sopivat = hoitajat.haeSopivat(k.luvat)
        hoitaja = min(sopivat, key=lambda k: hoitokerrat[k.nimi])
        hoitokerrat[hoitaja.nimi] += 1
        hoitovuorot[hoitaja.nimi].append(k.nimi)

    return template("hoitovuorot", hoitajat=hoitovuorot)


