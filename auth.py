import bcrypt
from bottle import request

class Auth(object):
    """Module for authenticating users and managing sessions."""
    def __init__(self, userbackend):
        self.users = userbackend

    def login(self, name, password):
        """Logs session in as a user, throws KeyError when no such user present"""
        s = request.environ["beaker.session"]
        user = self.users.byName(name)
        if user.pwhash == bcrypt.hashpw(password.encode(), user.salt):
            s["userid"] = user.userid
            return True
        raise KeyError("Wrong password")

    def loggedAs(self):
        """Return the name with which the current session is logged in as"""
        s = request.environ["beaker.session"]

        try:
            user = self.users.byId(s["userid"])
        except KeyError:
            return None
        return user.name

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
        self.users.addUser(name, salt, pwhash)
        
