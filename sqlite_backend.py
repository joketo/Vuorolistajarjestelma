import sqlite3
import json
from user import User
from hoitaja import Hoitaja
from asiakas import Asiakas

#TODO: tietokantakursorijuttujen siistiminen dekoraattorilla

class Users(object):
    def __init__(self, dbconnection):
        self.conn = dbconnection

    def byName(self, name):
        c = self.conn.cursor()
        c.execute("SELECT id, salt, hash from users where username=?", (name,))
        userid, salt, pwhash = c.fetchone()
        c.close()
        return User(userid, name, salt, pwhash)

    def byId(self, userid):
        c = self.conn.cursor()
        c.execute("SELECT username, salt, hash from users where id=?", (userid,))
        name, salt, pwhash = c.fetchone()
        c.close()
        return User(userid, name, salt, pwhash)
        

    def addUser(self, name, salt, pwhash):
        c = self.conn.cursor()
        c.execute("""INSERT INTO users (username, salt, hash)
                  VALUES (?, ?, ?)""", (name, salt, pwhash))
        self.conn.commit()
        c.close()

class Hoitajat(object):
    """Luokka Hoitaja-olioiden hakuun ja lisäykseen tietokannasta"""
    #TODO: luvat pitää nyt hakea lupataulusta
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def hae(self, hoitajaid=None, nimi=None):
        """Hakee tietokannasta hoitajan joko nimen tai id:n perusteella"""
        if not hoitajaid and not nimi:
            raise TypeError("hae tarvitsee argumentin hoitajaid tai nimi")

        c = self.conn.cursor()
        if hoitajaid:
            c.execute("SELECT rowid, nimi from hoitajat where rowid=?",(hoitajaid,))
        else:
            c.execute("SELECT rowid, nimi from hoitajat where nimi=?", (nimi,))
        hoitajaid, nimi = c.fetchone()
        luvat = self.haeLuvat(hoitajaid)
        return Hoitaja(hoitajaid, nimi, luvat)

    def kaikki(self):
        c = self.conn.cursor()
        c.execute("""SELECT rowid from hoitajat""")
        hoitajaidt = c.fetchall()
        c.close()
        #TODO: onko tämä hidasta?
        return [self.hae(hid[0]) for hid in hoitajaidt]

    def uusi(self, nimi, luvat):
        c = self.conn.cursor()
        c.execute("""INSERT INTO hoitajat (nimi)
                     VALUES (?)""", (nimi,))
        c.execute("SELECT rowid from hoitajat where nimi=?", (nimi,))
        hoitajaId = c.fetchone()
        c.close()
        self.conn.commit()
        self.luoLuvat(hoitajaId[0], luvat)

    def haeSopivat(self, luvat):
        """Palauttaa listan hoitajista jotka täyttävät annetut luvat"""
        #TODO: tee tämä näppärällä sql-haulla
        hoitsut = self.kaikki()
        return filter(lambda h: h.onkoLuvat(luvat), hoitsut)

    def haeLuvat(self, hoitajaId):
        c = self.conn.cursor()
        c.execute("""SELECT lupa from hoitajaluvat
                     where hoitajaid = ?""", (hoitajaId,))
        luvat = c.fetchall()
        c.close()
        return map(lambda a: a[0], luvat)

    def luoLuvat(self, hoitajaId, luvat):
        c = self.conn.cursor()
        for l in luvat:
            c.execute("""INSERT into hoitajaluvat (hoitajaid, lupa)
                         values (?,?)""", (hoitajaId, l))
        self.conn.commit()
        c.close()

class Asiakkaat(object):
    """Luokka asiakkaiden räpläykseen tietokantaan/kannasta"""
    def __init__(self, tkyhteys):
        self.conn = tkyhteys

    def hae(self, asiakasid=None, nimi=None):
        """Hakee tietokannasta asiakkaan joko nimen tai id:n perusteella"""
        if not asiakasid and not nimi:
            raise TypeError("hae tarvitsee argumentin asiakasid tai nimi")

        c = self.conn.cursor()
        if asiakasid:
            c.execute("SELECT rowid, nimi from asiakkaat where rowid=?",(asiakasid,))
        else:
            c.execute("SELECT rowid, nimi from asiakkaat where nimi=?", (nimi,))
        asiakasid, nimi = c.fetchone()
        luvat = self.haeLuvat(asiakasid)
        return Asiakas(asiakasid, nimi, luvat, None)

    def kaikki(self):
        c = self.conn.cursor()
        c.execute("""SELECT rowid from asiakkaat""")
        asiakasidt = c.fetchall()
        c.close()
        #TODO: onko tämä hidasta?
        return [self.hae(hid[0]) for hid in asiakasidt]

    def uusi(self, nimi, luvat):
        c = self.conn.cursor()
        c.execute("""INSERT INTO asiakkaat (nimi)
                     VALUES (?)""", (nimi,))
        asiakasId = c.lastrowid
        c.close()
        self.conn.commit()
        self.luoLuvat(asiakasId[0], luvat)

    def haeLuvat(self, asiakasId):
        c = self.conn.cursor()
        c.execute("""SELECT lupa from asiakasluvat
                     where asiakasid = ?""", (asiakasId,))
        luvat = c.fetchall()
        c.close()
        return map(lambda a: a[0], luvat)

    def luoLuvat(self, asiakasId, luvat):
        c = self.conn.cursor()
        for l in luvat:
            c.execute("""INSERT into asiakasluvat (asiakasid, lupa)
                         values (?,?)""", (asiakasId, l))
        c.close()
        self.conn.commit()

    def lisaaKaynti(self, asiakasid, kesto, luvat):
        c = self.conn.cursor()
        c.execute("""INSERT into kaynnit (asiakas, kesto)
                     values (?,?)""", (asiakasid, kesto))
        kayntiId = c.lastrowid
        c.close()
        self.conn.commit()
        for l in luvat:
            lisaaKayntiLupa(kayntiId, l)

    def lisaaKayntiLupa(kayntiId, lupa):
        c = self.conn.cursor()
        c.execute("""INSERT into kayntiluvat (kayntiid, lupa)
                     values (?,?)""", (kayntiId, lupa))
        c.close()


