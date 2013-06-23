from user import User
from hoitaja import Hoitaja
from asiakas import Asiakas
from kaynti import Kaynti


class Users(object):
    def __init__(self, dbconnection):
        self.conn = dbconnection

    def byName(self, name):
        userid, salt, pwhash = dbSelect(self.conn, "SELECT id, salt, hash from users where username=?", (name,))[0]
        return User(userid, name, salt, pwhash)

    def byId(self, userid):
        name, salt, pwhash = dbSelect(self.conn, "SELECT username, salt, hash from users where id=?", (userid,))[0]
        return User(userid, name, salt, pwhash)

    def addUser(self, name, salt, pwhash):
        dbInsert(self.conn, """INSERT INTO users (username, salt, hash)
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
        #TODO: transaktioi tämä
        """Poistaa tietokannasta nimen tai id:n perusteella"""
        if not hoitajaid and not nimi:
            raise TypeError("hae tarvitsee argumentin hoitajaid tai nimi")

        if hoitajaid:
             dbAction(self.conn, "DELETE FROM hoitajat id=?", (hoitajaid,))
        else:
            hoitajaid = dbSelect(self.conn, "SELECT id from hoitajat where nimi=?", 
                                 (nimi,))[0][0]
            dbAction(self.conn, "DELETE FROM hoitajat where nimi=?", (nimi,))

    def poistaLuvat(self, hoitajaid):
         dbAction(self.conn, "DELETE FROM hoitajaluvat where hoitajaid=?", (hoitajaid,))

    def kaikki(self):
        hoitajaidt = dbSelect(self.conn, """SELECT id from hoitajat""")
        return [self.hae(hid[0]) for hid in hoitajaidt]

    def uusi(self, nimi, luvat):
        hoitajaId = dbInsert(self.conn, """INSERT INTO hoitajat (nimi)
                     VALUES (?)""", (nimi,))
        self.luoLuvat(hoitajaId, luvat)

    def haeSopivat(self, luvat):
        """Palauttaa listan hoitajista jotka täyttävät annetut luvat"""
        #TODO: tee tämä näppärällä sql-haulla
        hoitsut = self.kaikki()
        return filter(lambda h: h.onkoLuvat(luvat), hoitsut)

    def haeSopivatKaynnilla(self, kayntiid):
        """Palauttaa listan hoitajista, joilla on sopivat luvat annetun 
        käynnin hoitamiseksi."""

        dbAction(self.conn,
                 """
                 CREATE TEMP TABLE vaaditut AS 
                 SELECT lupaid FROM kayntiluvat
                 WHERE kayntiid=?
                 """, (kayntiid,))
 
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
        dbAction(self.conn,"DROP TABLE vaaditut")

        print(kayntiid, ": ", hoitajaidt)
        hoitajat = [self.hae(hoitajaid=hid[0]) for hid in hoitajaidt]
        return hoitajat
        

    def haeLuvat(self, hoitajaId):
        luvat = dbSelect(self.conn, """SELECT lupaid, lupa from hoitajaluvat, luvat
                                       WHERE  lupaid = luvat.id
                                       AND    hoitajaid = ?""", (hoitajaId,))
        return luvat

    def luoLuvat(self, hoitajaId, luvat):
        for l in luvat:
            dbInsert(self.conn, """INSERT into hoitajaluvat (hoitajaid, lupaid)
                         values (?,?)""", (hoitajaId, l))
        


class Asiakkaat(object):
    """Luokka asiakkaiden räpläykseen tietokantaan/kannasta"""
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def hae(self, asiakasid=None, nimi=None):
        """Hakee tietokannasta asiakkaan joko nimen tai id:n perusteella"""
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
        asiakasidt = dbSelect(self.conn, "SELECT id from asiakkaat")
        return [self.hae(aid[0]) for aid in asiakasidt]

    def uusi(self, nimi):
        dbInsert(self.conn, """INSERT INTO asiakkaat (nimi)
                               VALUES (?)""", (nimi,))

    def lisaaKaynti(self, asiakasid, kesto, aika, paiva, luvat):
        kayntiId = dbInsert(self.conn, """INSERT into kaynnit (asiakasid, kestoid, aikaid, paivaid)
                                          values (?,?,?,?)""",
                                       (asiakasid, kesto, aika, paiva))
        for l in luvat:
            self.lisaaKayntiLupa(kayntiId, l)

    def haeKaynnit(self, asiakasid):
        kayntirivit = dbSelect(self.conn, 
                               """SELECT kaynnit.id, asiakasid, paiva, aika, kesto FROM kaynnit, ajat, kestot, paivat
                                  WHERE  paivaid=paivat.id
                                  AND    aikaid=ajat.id
                                  AND    kestoid=kestot.id                               
                                  AND    asiakasid = ?
                               """, (asiakasid,))
        kaynnit = []
        for rivi in kayntirivit:
            luvat = self.haeKayntiLuvat(rivi[0])
            luvat = [l[1] for l in luvat]
            kaynnit.append(Kaynti(rivi[0], self, rivi[1], luvat, rivi[2], rivi[3], rivi[4]))
        return kaynnit

    def kaikkiKaynnit(self):
        kayntirivit = dbSelect(self.conn,
                               """SELECT kaynnit.id, asiakasid, paiva, aika, kesto FROM kaynnit, ajat, kestot, paivat
                                  WHERE  paivaid=paivat.id
                                  AND    aikaid=ajat.id
                                  AND    kestoid=kestot.id""")
        kaynnit = []
        for rivi in kayntirivit:
            luvat = self.haeKayntiLuvat(rivi[0])
            luvat = [l[1] for l in luvat]
            kaynnit.append(Kaynti(rivi[0], self, rivi[1], luvat, rivi[2], rivi[3], rivi[4]))
        return kaynnit

    def lisaaKayntiLupa(self, kayntiId, lupa):
        dbInsert(self.conn, """INSERT into kayntiluvat (kayntiid, lupaid)
                          values (?,?)""", (kayntiId, lupa))

    def haeKayntiLuvat(self, kayntiId):
        luvat = dbSelect(self.conn,
                         """SELECT lupaid, lupa from kayntiluvat, luvat
                            WHERE lupaid = luvat.id AND kayntiid=?""", (kayntiId,))
        return [l for l in luvat]
        
    def poistaAsiakas(self, asiakasId):
        dbAction(self.conn, "DELETE FROM asiakkaat where id=?", (asiakasId,))
        
    def poistaKaynti(self, kayntiId):
         dbAction(self.conn, "DELETE FROM kaynnit where id=?", (kayntiId,))
                
    def poistaKayntiLuvat(self, kayntiId):
         dbAction(self.conn, "DELETE FROM kayntiluvat where kayntiid=?", (kayntiId,))


class Vakiot(object):
    """Luokka tietokannassa olevien arvojen tekstimuotoisten nimien hakuun"""
    
    def __init__(self, tkyhteys):
        self.conn =tkyhteys

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



def dbInsert(conn, insertstr, params=None):
    """Suorita annettu insert-tyyppinen tietokantatoiminto ja palauta lisätyn rivin id"""
    c = conn.cursor()
    if params:
        c.execute(insertstr, params)
    else:
        c.execute(insertstr)
    rowid = c.lastrowid
    c.close
    conn.commit()
    return rowid

def dbAction(conn, insertstr, params=None):
    """Järkevämmän kuuloinen alias dbInsertille poistoja varten"""
    return dbInsert(conn, insertstr, params)


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


