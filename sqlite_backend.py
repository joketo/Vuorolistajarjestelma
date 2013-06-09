import sqlite3
import json
from user import User
from hoitaja import Hoitaja

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
        self.yhteys = tkyhteys

    def idnMukaan(self, hoitsuid):
        c = self.conn.cursor()
        c.execute("SELECT name from hoitajat where id=?",(hoitsuid,))
        nimi, luvat = c.fetchone()
        luvat = json.reads(luvat)
        c.close()

    def nimenMukaan(self, nimi):
        c = self.conn.cursor()
        c.execute("SELECT id, from hoitajat where name=?", (nimi,))
        hoitsuid, luvat = c.fetchone()
        luvat = json.reads(luvat)
        c.close()

        return Hoitaja(hoitsuid, nimi, luvat)

    def uusi(self, nimi, luvat):
        c = self.conn.cursor()
        c.execute("""INSERT INTO hoitajat (name)
                     VALUES (?)""", (nimi,))
        c.commit()
        c.close()

    def haeLuvat(self, hoitajaId):
        c = self.conn.cursor()
        c.execute("""SELECT lupa from hoitajaluvat
                     where hoitajaid = ?""", (hoitajaId,))
        luvat = c.fetchall()
        c.close()
        return luvat

    def luoLuvat(self, hoitajaId, luvat):
        c = self.conn.cursor()
        for l in luvat:
            c.execute("""INSERT int hoitajaluvat (hoitajaid, lupa)
                         values (?,?)""", (hoitajaId, l))
        c.commit()
        c.close()

        
