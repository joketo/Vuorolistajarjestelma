from bottle import route, run, template, response, request, redirect, static_file, app
from main import auth, conn, hoitajat, asiakkaat
from sqlite3 import IntegrityError


def loginVaaditaan():
    if not auth.isLogged():
        redirect("/login")
    

@route("/")
def etusivu():
    loginVaaditaan()
    nimi = auth.loggedAs()
    return template("front", nimi=nimi)
    
@route("/test")
def test():
    app().message = "testi toimii"
    return "test"


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@route("/login")
def login_form():
    return template("loginForm", virheviesti=None)


@route("/login", method="POST")
def login_submit():
    name = request.forms.getunicode("name")
    password = request.forms.getunicode("password")
    
    try:
        auth.login(name, password)
    # Innokas except jottei loginin epäonnistumisviesti anna vihjeitä hyökkääjälle
    except:
        return template("loginForm", virheviesti="Kirjautuminen epäonnistui")
    redirect("/")


@route("/logout")
def logout():
    auth.logout()
    return template("logout")


@route("/register")
def register_get():
    return template("register", virheviesti=None)


@route("/register", method="POST")
def register_post():
    name = request.forms.getunicode("name")
    password1 = request.forms.getunicode("password1")
    password2 = request.forms.getunicode("password2")
    
    if password1 != password2:
        return template("register", virheviesti="Salasanat eivät täsmää")
    try:
        auth.register(name, password1)
    except IntegrityError:
        return template("register", virheviesti="Valitsemasi käyttäjätunnus on jo käytössä")
    return template("rekOK")


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
    try:
        hoitajat.uusi(nimi, luvat)
    except:
        return template("hoitajat",hoitajat=hoitajat.kaikki(),
                        virheviesti="Hoitajan lisäys epäonnistui")
    redirect("/hoitajat")


@route("/poistaHoitaja", method="POST")
def poistaHoitaja():
    loginVaaditaan()
    hoitaja = request.forms.getunicode("poistettava")
    print(hoitaja)
    hoitajat.poista(nimi=hoitaja)
    redirect("/hoitajat")


@route("/asiakkaat", method="POST")
def asiakkaat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    if not nimi:
        return template("asiakkaanHallinta", asiakkaat=asiakkaat.kaikki(), 
                        virheviesti="Asiakkaalla tulee olla nimi")
    try:
        asiakkaat.uusi(nimi)
    except Exception:
        return template("asiakkaanHallinta", asiakkaat=asiakkaat.kaikki(), 
                        virheviesti="Asiakkaan lisäys epäonnistui")
        
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
    loginVaaditaan()
    # TODO: luo hoitovuorot jossain muualla
    # jakaa hoitovuoron mahdollisista hoitajista aina sille, jolla on
    # vähiten käyntejä
    hoitokerrat = {h: 0 for h in map(lambda h: h.nimi, hoitajat.kaikki())}
    hoitovuorot = {h: [] for h in map(lambda h: h.nimi, hoitajat.kaikki())}
    for k in asiakkaat.kaikkiKaynnit():
        sopivat = hoitajat.haeSopivatKaynnilla(k.kayntiid)
        hoitaja = min(sopivat, key=lambda k: hoitokerrat[k.nimi])
        hoitokerrat[hoitaja.nimi] += 1
        hoitovuorot[hoitaja.nimi].append(k)

    return template("hoitovuorot", hoitajat=hoitovuorot)

@route("/poistaKaynti", method="POST")
def poistaKaynti():
    kayntiId = request.forms.getunicode("kayntiid")
    asiakkaat.poistaKaynti(kayntiId)
    print (kayntiId)
    redirect("/asiakkaanHallinta")


