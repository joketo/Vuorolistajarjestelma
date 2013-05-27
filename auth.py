import bcrypt
from bottle import request

class Auth(object):
    """Module for authenticating users and managing sessions."""
    def __init__(self, dbhandle):
        self.db = dbhandle

    def login(self, name, password):
        """Logs session in as a user, throws KeyError when no such user present"""
        s = request.environ["beaker.session"]
        c = self.db.cursor()
        c.execute("SELECT id, salt, hash from users where username=?", (name,))
        userid, salt, pwhash = c.fetchone()
        c.close()
        if pwhash == bcrypt.hashpw(password.encode(), salt):
            s["userid"] = userid
            return True
        return False

    def loggedAs(self):
        """Return the name with wich the current session is logged in as"""
        s = request.environ["beaker.session"]
        c = self.db.cursor()
        c.execute("SELECT username from users where id=?", (s["userid"],))
        name, = c.fetchone()
        c.close()
        return name

    def isLogged(self):
        s = request.environ["beaker.session"]
        if "userid" in s:
            return True
        return False

    def logout(self):
        s = request.environ["beaker.session"]
        if self.isLogged():
            s.pop("userid")

    def register(self, name, password):
        salt = bcrypt.gensalt()
        pwhash = bcrypt.hashpw(password.encode(), salt)

        c = self.db.cursor()
        c.execute("""INSERT INTO users (username, salt, hash)
                  VALUES (?, ?, ?)""", (name, salt, pwhash))
        self.db.commit()
        c.close()
        #TODO: handle exceptions
