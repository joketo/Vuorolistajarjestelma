"""
routes.py sisältää Bottlen handlerit eri osoitteille
"""

from bottle import route, template, request, redirect, static_file, app
from sqlite3 import IntegrityError


def loginVaaditaan():
    return
    """Redirectaa login-sivulle jos käyttäjä ei ole kirjautunut"""
    if not app().auth.isLogged():
        redirect("/login")

def virheViesti():
    """Hae sessioon liittyvä virheviesti ja palauta se jos sellainen on. None muuten"""
    s = request.environ["beaker.session"]
    viesti = None if not "virheviesti" in s else s["virheviesti"]
    s["virheviesti"] = None
    return viesti

def asetaVirheViesti(viesti):
    request.environ["beaker.session"]["virheviesti"] = viesti

@route("/")
def etusivu():
    virheviesti = virheViesti()
    loginVaaditaan()
    nimi = app().auth.loggedAs()
    return template("front", nimi=nimi, virheviesti=virheviesti)

    
@route('/static/<filepath:path>')
def server_static(filepath):
    """Staattisten tiedostojen jako"""
    return static_file(filepath, root='static')


@route("/login")
def login():
    virheviesti = virheViesti()
    return template("loginForm", virheviesti=virheviesti)


@route("/login", method="POST")
def login_post():
    name = request.forms.getunicode("name")
    password = request.forms.getunicode("password")
    
    try:
        app().auth.login(name, password)
    # Innokas except jottei loginin epäonnistumisviesti anna vihjeitä hyökkääjälle
    except Exception:
        asetaVirheViesti("Kirjautuminen epäonnistui")
        redirect("/login")
    redirect("/")


@route("/logout")
def logout():
    app().auth.logout()
    return template("logout")


@route("/register")
def register():
    virheviesti=virheViesti()
    return template("register", virheviesti=virheviesti)


@route("/register", method="POST")
def register_post():
    name = request.forms.getunicode("name")
    password1 = request.forms.getunicode("password1")
    password2 = request.forms.getunicode("password2")
    
    if password1 != password2:
        asetaVirheViesti("Salasanat eivät täsmää")
        redirect("/register")
    try:
        app().auth.register(name, password1)
    except IntegrityError:
        asetaVirheViesti("Valitsemasi käyttäjätunnus on jo käytössä")
        redirect("/register")
    return template("rekOK")


@route("/hoitajat")
def hoitajat():
    """Hoitajien hallintasivu"""
    loginVaaditaan()
    virheviesti = virheViesti()
    hoitsut = app().hoitajat.kaikki()
    luvat = app().vakiot.luvat()
    return template("hoitajat", hoitajat=hoitsut, luvat=luvat, virheviesti=virheviesti)
    

@route("/hoitajat", method="POST")
def hoitajat_post():
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    luvat = request.forms.getall("lupa")
    # ei ole getallunicode()-metodia, muuta kaikki unicodeksi
    luvat = [l.encode("latin-1").decode("utf8") for l in luvat]
    try:
        app().hoitajat.uusi(nimi, luvat)
    except Exception:
        asetaVirheViesti("Hoitajan lisäys epäonnistui")
        redirect("/hoitajat")
    redirect("/hoitajat")


@route("/poistaHoitaja", method="POST")
def poistaHoitaja():
    loginVaaditaan()
    hoitaja = request.forms.getunicode("poistettava")
    app().hoitajat.poista(nimi=hoitaja)
    redirect("/hoitajat")


@route("/luoAsiakas", method="POST")
def asiakkaat_post():
    """Luo uusi asiakas"""
    loginVaaditaan()
    nimi = request.forms.getunicode("nimi")
    if not nimi:
        asetaVirheViesti("Asiakkaalla tulee olla nimi")
        redirect("asiakkaanHallinta")
    try:
        app().asiakkaat.uusi(nimi)
    except Exception:
        asetaVirheViesti("Asiakkaan lisäys epäonnistui")
    redirect("/asiakkaanHallinta")
    
    
@route("/asiakkaanHallinta")
def asiakkaanHallinta():
    """Asiakkaiden hallintasivu"""
    virheviesti = virheViesti()

    loginVaaditaan()
    asiakkaat = app().asiakkaat.kaikki()
    luvat = app().vakiot.luvat()
    paivat = app().vakiot.paivat()
    ajat = app().vakiot.ajat()
    kestot = app().vakiot.kestot()
    return template("asiakkaanHallinta", asiakkaat=asiakkaat, luvat=luvat, ajat=ajat, 
                    kestot=kestot, paivat=paivat, virheviesti=virheviesti)
    

@route("/lisaaVuoro", method="POST")
def lisaaVuoro_post():
    """Lisää uusi hoitovuoro"""
    loginVaaditaan()
    request.forms.recode_unicode = True
    asiakasid = request.forms.getunicode("asiakas")
    paiva = request.forms.getunicode("paiva")
    aika = request.forms.getunicode("aika")
    kesto = request.forms.getunicode("kesto")
    luvat = request.forms.getall("lupa")
    # kai tähän pitää olla fiksumpi tapa, ei ole getallunicode()-metodia...
    luvat = [l.encode("latin-1").decode("utf8") for l in luvat]
    try:
        app().asiakkaat.lisaaKaynti(asiakasid, kesto, aika, paiva, luvat)
    except IntegrityError:
        asetaVirheViesti("Käynnin lisäys epäonnistui")
        
    redirect("/asiakkaanHallinta")


@route("/hoitovuorot")
def hoitovuorot():
    """Jaa ja näytä hoitovuorot. Jakaa hoitovuorot ainoastaan niiden 
       lukumäärän perusteella. Voisi tehdä myös keston perusteella mutta 
       käyntien kestot ovat pääsääntöisesti lyhyitä joten paikasta toiseen 
       kulkemisen viemä aika on huomattava.
    """
    loginVaaditaan()
    # jakaa hoitovuoron mahdollisista hoitajista aina sille, jolla on
    # vähiten käyntejä. Voisi jakaa ajan perusteella mutta käynnit
    # ovat lyhyitä verrattuna liikkumisaikaan
    hoitokerrat = {h: 0 for h in map(lambda h: h.nimi, app().hoitajat.kaikki())}
    hoitovuorot = {h: [] for h in map(lambda h: h.nimi, app().hoitajat.kaikki())}
    vaillaHoitajaa = []
    virheviesti = None

    for k in app().asiakkaat.kaikkiKaynnit():
        sopivat = app().hoitajat.haeSopivatKaynnilla(k.kayntiid)
        if not sopivat: #ei löytynyt sopivia hoitajia
            vaillaHoitajaa.append(k.asiakasnimi + ": " + str(k))
            continue
        hoitaja = min(sopivat, key=lambda k: hoitokerrat[k.nimi])
        hoitokerrat[hoitaja.nimi] += 1
        hoitovuorot[hoitaja.nimi].append(k)

    if vaillaHoitajaa:
        virheviesti = "Seuraaville käynneille ei lyötynyt hoitajaa: " + "; ".join(vaillaHoitajaa)
    return template("hoitovuorot", hoitajat=hoitovuorot, virheviesti=virheviesti)


@route("/poistaKayntiTaiAsiakas", method="POST")
def poistaKaynti():
    kayntiId = request.forms.getunicode("kayntiid")
    asiakasId = request.forms.getunicode("asiakasid")
    if kayntiId:
        app().asiakkaat.poistaKaynti(kayntiId)
    if asiakasId:
        app().asiakkaat.poistaAsiakas(asiakasId)
    redirect("/asiakkaanHallinta")
