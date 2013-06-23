from bottle import route, run, template, response, request, redirect, static_file, app
from sqlite3 import IntegrityError


def loginVaaditaan():
    return
    if not app().auth.isLogged():
        redirect("/login")

@route("/test")
def test():
    return str(dir(app()))

@route("/")
def etusivu():
    loginVaaditaan()
    nimi = app().auth.loggedAs()
    return template("front", nimi=nimi)

    
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
        app().auth.login(name, password)
    # Innokas except jottei loginin epäonnistumisviesti anna vihjeitä hyökkääjälle
    except:
        return template("loginForm", virheviesti="Kirjautuminen epäonnistui")
    redirect("/")


@route("/logout")
def logout():
    app().auth.logout()
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
        app().auth.register(name, password1)
    except IntegrityError:
        return template("register", virheviesti="Valitsemasi käyttäjätunnus on jo käytössä")
    return template("rekOK")


@route("/hoitajat")
def hoitajat_get():
    loginVaaditaan()
    hoitsut = app().hoitajat.kaikki()
    luvat = app().vakiot.luvat()
    return template("hoitajat", hoitajat=hoitsut, luvat=luvat)
    

@route("/hoitajat", method="POST")
def hoitajat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    luvat = request.forms.getall("lupa")
    # kai tähän pitää olla fiksumpi tapa, ei ole getallunicode()-metodia...
    luvat = [l.encode("latin-1").decode("utf8") for l in luvat]
#    try:
    app().hoitajat.uusi(nimi, luvat)
#    except Exception:
#        return template("hoitajat",hoitajat=app().hoitajat.kaikki(),
#                        virheviesti="Hoitajan lisäys epäonnistui")
    redirect("/hoitajat")


@route("/poistaHoitaja", method="POST")
def poistaHoitaja():
    loginVaaditaan()
    hoitaja = request.forms.getunicode("poistettava")
    print(hoitaja)
    app().hoitajat.poista(nimi=hoitaja)
    redirect("/hoitajat")


@route("/asiakkaat", method="POST")
def asiakkaat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    if not nimi:
        return template("asiakkaanHallinta", asiakkaat=app().asiakkaat.kaikki(), 
                        virheviesti="Asiakkaalla tulee olla nimi")
    try:
        app().asiakkaat.uusi(nimi)
    except Exception:
        return template("asiakkaanHallinta", asiakkaat=app().asiakkaat.kaikki(), 
                        virheviesti="Asiakkaan lisäys epäonnistui")
        
    redirect("/asiakkaanHallinta")
    
    
@route("/asiakkaanHallinta")
def asiakkaanHallinta():
    loginVaaditaan()
    asiakkaat = app().asiakkaat.kaikki()
    luvat = app().vakiot.luvat()
    paivat = app().vakiot.paivat()
    ajat = app().vakiot.ajat()
    kestot = app().vakiot.kestot()
    return template("asiakkaanHallinta", asiakkaat=asiakkaat, luvat=luvat, ajat=ajat, kestot=kestot, paivat=paivat)
    

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
    app().asiakkaat.lisaaKaynti(asiakasid, kesto, aika, paiva, luvat)
    redirect("/asiakkaanHallinta")


@route("/hoitovuorot")
def hoitovuorot():
    loginVaaditaan()
    # TODO: luo hoitovuorot jossain muualla
    # jakaa hoitovuoron mahdollisista hoitajista aina sille, jolla on
    # vähiten käyntejä
    hoitokerrat = {h: 0 for h in map(lambda h: h.nimi, app().hoitajat.kaikki())}
    hoitovuorot = {h: [] for h in map(lambda h: h.nimi, app().hoitajat.kaikki())}
    for k in app().asiakkaat.kaikkiKaynnit():
        sopivat = app().hoitajat.haeSopivatKaynnilla(k.kayntiid)
        hoitaja = min(sopivat, key=lambda k: hoitokerrat[k.nimi])
        hoitokerrat[hoitaja.nimi] += 1
        hoitovuorot[hoitaja.nimi].append(k)

    return template("hoitovuorot", hoitajat=hoitovuorot)

@route("/poistaKaynti", method="POST")
def poistaKaynti():
    kayntiId = request.forms.getunicode("kayntiid")
    app().asiakkaat.poistaKaynti(kayntiId)
    print (kayntiId)
    redirect("/asiakkaanHallinta")


