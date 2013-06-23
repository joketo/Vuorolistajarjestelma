"""
Tämä moduuli sisältää llioita sql-tietokannan käyttöä varten.
"""

from user import User
from hoitaja import Hoitaja
from asiakas import Asiakas
from kaynti import Kaynti


class Users(object):
    """Luokka tietokannan käyttäjien hallintaan"""
    def __init__(self, dbconnection):
        self.conn = dbconnection

    def byName(self, name):
        userid, salt, pwhash = dbSelect(self.conn, "SELECT id, salt, hash from users where username=?", (name,))[0]
        return User(userid, name, salt, pwhash)

    def byId(self, userid):
        name, salt, pwhash = dbSelect(self.conn, "SELECT username, salt, hash from users where id=?", (userid,))[0]
        return User(userid, name, salt, pwhash)

    def addUser(self, name, salt, pwhash):
        dbAction(self.conn, """INSERT INTO users (username, salt, hash)
                  VALUES (?, ?, ?)""", (name, salt, pwhash))


class Hoitajat(object):
    """Luokka Hoitaja-olioiden hakuun ja lisäykseen tietokannasta"""
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def hae(self, hoitajaid=None, nimi=None):
        """Hakee tietokannasta hoitajan joko nimen tai id:n perusteella"""
        if not hoitajaid and not nimi:
            raise TypeError("hae tarvitsee argumentin hoitajaid tai nimi")

        if hoitajaid:
            hoitajaid, nimi = dbSelect(self.conn, "SELECT id, nimi from hoitajat where id=?", (hoitajaid,))[0]
        else:
            hoitajaid, nimi = dbSelect(self.conn, "SELECT id, nimi from hoitajat where nimi=?", (nimi,))[0]
        luvat = self.haeLuvat(hoitajaid)
        return Hoitaja(hoitajaid, nimi, [a[1] for a in luvat])

    def poista(self, hoitajaid=None, nimi=None):
        """Poistaa tietokannasta nimen tai id:n perusteella."""
        if not hoitajaid and not nimi:
            raise TypeError("hae tarvitsee argumentin hoitajaid tai nimi")

        if hoitajaid:
            dbAction(self.conn, "DELETE FROM hoitajat id=?", (hoitajaid,))
        else:
            dbAction(self.conn, "DELETE FROM hoitajat where nimi=?", (nimi,))

    def kaikki(self):
        """Palauttaa Hoitaja-olion jokaista taulun hoitajaa kohden"""
        hoitajaidt = dbSelect(self.conn, """SELECT id from hoitajat""")
        return [self.hae(hid[0]) for hid in hoitajaidt]

    def uusi(self, nimi, lupaidt):
        """Luo uusi hoitaja"""
        hoitajaId = dbAction(self.conn, """INSERT INTO hoitajat (nimi)
                     VALUES (?)""", (nimi,))
        self.luoLuvat(hoitajaId, lupaidt)

    def haeSopivatKaynnilla(self, kayntiid):
        """Palauttaa listan hoitajista, joilla on sopivat luvat annetun 
        käynnin hoitamiseksi."""

        # luo väliaikainen taulu ettei tarvitse hakea näitä useaan otteeseen
        dbAction(self.conn,
                 """
                 CREATE TEMP TABLE vaaditut AS 
                 SELECT lupaid FROM kayntiluvat
                 WHERE kayntiid=?
                 """, (kayntiid,))
 
        # idea: hae sellaiset hoitajaid:t joilla lupien ja vaadittujen
        # lupien leikkaus on kooltaan yhtä suuri kuin vaaditut luvat
        hoitajaidt = dbSelect(self.conn,
                              """
                              SELECT   hoitajaid hid
                              FROM     hoitajaluvat
                              GROUP BY hoitajaid
                              HAVING   (SELECT count(*) 
                                        FROM hoitajaluvat 
                                        JOIN vaaditut USING (lupaid)
                                        WHERE hoitajaid = hid) =
                                       (SELECT count(*)
                                        FROM vaaditut)
                              """)
        dbAction(self.conn, "DROP TABLE vaaditut")

        # luo hoitajaoliot
        hoitajat = [self.hae(hoitajaid=hid[0]) for hid in hoitajaidt]
        return hoitajat

    def haeLuvat(self, hoitajaId):
        """Hae hoitajaid:n perusteella luvat. Palauttaa listan (id, lupa)-pareja"""
        luvat = dbSelect(self.conn, """SELECT lupaid, lupa from hoitajaluvat, luvat
                                       WHERE  lupaid = luvat.id
                                       AND    hoitajaid = ?""", (hoitajaId,))
        return luvat

    def luoLuvat(self, hoitajaId, lupaidt):
        """Luo kantaan annetunlaiset lupa-rivit"""
        for l in lupaidt:
            dbAction(self.conn, """INSERT into hoitajaluvat (hoitajaid, lupaid)
                         values (?,?)""", (hoitajaId, l))
        

class Asiakkaat(object):
    """Luokka asiakkaiden ja niihin liittyvien käyntien räpläykseen 
    tietokantaan/kannasta."""
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def hae(self, asiakasid=None, nimi=None):
        """Hakee tietokannasta asiakkaan joko nimen tai id:n perusteella. Palauttaa Asiakas-olion"""
        if not asiakasid and not nimi:
            raise TypeError("hae tarvitsee argumentin asiakasid tai nimi")

        # TODO: heittele virhe jos ei löydy moisen nimistä/id:istä
        if asiakasid:
            asiakasid, nimi = dbSelect(self.conn, 
                                       "SELECT id, nimi from asiakkaat where id=?",
                                       (asiakasid,))[0]
        else:
            asiakasid, nimi = dbSelect(self.conn, 
                                       "SELECT id, nimi from asiakkaat where nimi=?",
                                       (nimi,))[0]
        kaynnit = self.haeKaynnit(asiakasid)
        return Asiakas(asiakasid, nimi, kaynnit)

    def kaikki(self):
        """Palauttaa listan, jossa on Asiakas-olio jokaista asiakasriviä kohden"""
        asiakasidt = dbSelect(self.conn, "SELECT id from asiakkaat")
        return [self.hae(aid[0]) for aid in asiakasidt]

    def uusi(self, nimi):
        """Luo kantaan uusi asiakas"""
        dbAction(self.conn, """INSERT INTO asiakkaat (nimi)
                               VALUES (?)""", (nimi,))

    def lisaaKaynti(self, asiakasid, kestoid, aikaid, paivaid, lupaidt):
        """Lisää tietokantaan käynnin jolla on annetut arvot."""
        kayntiId = dbAction(self.conn, """INSERT into kaynnit (asiakasid, kestoid, aikaid, paivaid)
                                          values (?,?,?,?)""",
                                       (asiakasid, kestoid, aikaid, paivaid))
        for l in lupaidt:
            self.lisaaKayntiLupa(kayntiId, l)

    def haeKaynnit(self, asiakasid):
        """Palauttaa listan, jossa on Kaynti-olio jokaista annetun asiakkaan käyntiä kohden"""
        kayntirivit = dbSelect(self.conn, 
                               """SELECT kaynnit.id, asiakasid, paiva, aika, kesto FROM kaynnit, ajat, kestot, paivat
                                  WHERE  paivaid=paivat.id
                                  AND    aikaid=ajat.id
                                  AND    kestoid=kestot.id                               
                                  AND    asiakasid = ?
                               """, (asiakasid,))
        # Luo käyntiriveistä kaynti-oliot
        kaynnit = []
        for rivi in kayntirivit:
            luvat = self.haeKayntiLuvat(rivi[0])
            luvat = [l[1] for l in luvat]
            kaynnit.append(Kaynti(rivi[0], rivi[1], luvat, rivi[2], rivi[3], rivi[4]))
        return kaynnit

    def kaikkiKaynnit(self):
        """Palauttaa listan jossa on Kaynti-olio jokaista käyntiä kohden"""
        kayntirivit = dbSelect(self.conn,
                               """SELECT kaynnit.id, asiakasid, paiva, aika, kesto FROM kaynnit, ajat, kestot, paivat
                                  WHERE  paivaid=paivat.id
                                  AND    aikaid=ajat.id
                                  AND    kestoid=kestot.id""")
        # Luo käyntiriveistä kaynti-oliot
        kaynnit = []
        for rivi in kayntirivit:
            luvat = self.haeKayntiLuvat(rivi[0])
            luvat = [l[1] for l in luvat]
            kaynnit.append(Kaynti(rivi[0], rivi[1], luvat, rivi[2], rivi[3], rivi[4]))
        return kaynnit

    def lisaaKayntiLupa(self, kayntiId, lupaid):
        """Lisää annetulle käynnille lupavaatimus"""
        dbAction(self.conn, """INSERT into kayntiluvat (kayntiid, lupaid)
                          values (?,?)""", (kayntiId, lupaid))

    def haeKayntiLuvat(self, kayntiId):
        """Hae annetun käynnin vaaditut luvat"""
        luvat = dbSelect(self.conn,
                         """SELECT lupaid, lupa from kayntiluvat, luvat
                            WHERE lupaid = luvat.id AND kayntiid=?""", (kayntiId,))
        return [l for l in luvat]

    # Tietokannassa on delete cascade eli ok vain poistaa näin
    def poistaAsiakas(self, asiakasId):
        dbAction(self.conn, "DELETE FROM asiakkaat where id=?", (asiakasId,))
        
    def poistaKaynti(self, kayntiId):
        dbAction(self.conn, "DELETE FROM kaynnit where id=?", (kayntiId,))
                
    def poistaKayntiLuvat(self, kayntiId):
        dbAction(self.conn, "DELETE FROM kayntiluvat where kayntiid=?", (kayntiId,))


class Vakiot(object):
    """Luokka tietokannassa olevien arvojen tekstimuotoisten nimien hakuun
       Kaikki metodit palauttavat listan (id, arvo)-pareja.
    """
    
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def paivat(self):
        paivat = dbSelect(self.conn, "SELECT id, paiva FROM paivat ORDER BY id")
        return paivat

    def luvat(self):
        luvat = dbSelect(self.conn, "SELECT id, lupa FROM luvat ORDER BY id")
        return luvat

    def ajat(self):
        ajat = dbSelect(self.conn, "SELECT id, aika FROM ajat ORDER BY id")
        print("aika", ajat)
        return ajat

    def kestot(self):
        kestot = dbSelect(self.conn, "SELECT id, kesto FROM kestot ORDER BY id")
        return kestot


def dbAction(conn, insertstr, params=None):
    """Suorita annettu tietokantatoiminto ja palauta lisätyn rivin id"""
    c = conn.cursor()
    if params:
        c.execute(insertstr, params)
    else:
        c.execute(insertstr)
    rowid = c.lastrowid
    c.close()
    conn.commit()
    return rowid


def dbSelect(conn, selectstr, params=None):
    """Suorita annettu tietokantahaku ja palauta tietokannalta tulleet arvot"""
    c = conn.cursor()
    if params:
        c.execute(selectstr, params)
    else:
        c.execute(selectstr)
    tulos = c.fetchall()
    c.close()
    return tulos
