import sqlite3
import json
from user import User
from hoitaja import Hoitaja

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

    def kaikkiHoitajat(self):
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
        if not asiakasaid and not nimi:
            raise TypeError("hae tarvitsee argumentin asiakasid tai nimi")

        c = self.conn.cursor()
        if hoitajaid:
            c.execute("SELECT rowid, nimi from asiakkaat where rowid=?",(hoitajaid,))
        else:
            c.execute("SELECT rowid, nimi from asiakkaat where nimi=?", (nimi,))
        asiakasid, nimi = c.fetchone()
        luvat = self.haeLuvat(asiakas)
        return Asiakas(asiakasid, nimi, luvat)

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
        c.execute("SELECT rowid from asiakkaat where nimi=?", (nimi,))
        asiakasId = c.fetchone()
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
        self.conn.commit()
        c.close()


        
        
                      

        
