import bcrypt
from bottle import request

class User(object):
    def __init__(self, name, passwd, sid=None):
        """User class, params:
        name: user name
        salt: salt for password hash :: builtins.bytes
        pwhash: bcrypt.hashpw(salt, password) :: builtins.bytes
        """
        self.name = name
        self.salt = bcrypt.gensalt()
        self.pwhash = bcrypt.hashpw(passwd.encode(), self.salt)


class Auth(object):
    """Module for authenticating users and managing sessions."""
    def __init__(self):
        #test users-dict
        #TODO: näihin hommiin tietokantaa
        self.users = {"pekka":User("pekka", "salasana")} 

    def login(self, name, password):
        """Logs session in as a user, throws KeyError when no such user present"""
        s = request.environ["beaker.session"]
        user = self.users[name]
        if user.pwhash == bcrypt.hashpw(password.encode(), user.salt):
            s["name"] = name
            return True
        return False

    def loggedAs(self):
        """Return the name with wich the current session is logged in as"""
        s = request.environ["beaker.session"]
        return s["name"]

    def isLogged(self):
        s = request.environ["beaker.session"]
        if "name" in s:
            return True
        return False

    def logout(self):
        s = request.environ["beaker.session"]
        s.pop("name")

    def register(self, uname, passwd):
        if uname in self.users:
            raise Exception("Can't make duplicate user")
        newUser = User(uname, passwd)
