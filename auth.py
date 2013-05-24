import bcrypt

class User(object):
    def __init__(self, name, passwd, sid=None):
        """User class, params:
        name: user name
        salt: salt for password hash :: builtins.bytes
        pwhash: bcrypt.hashpw(salt, password) :: builtins.bytes
        sid: session id
        """

        self.name = name
        self.salt = bcrypt.gensalt()
        self.pwhash = bcrypt.hashpw(passwd.encode(), self.salt)
        self.sid = sid

class Auth(object):
    """Module for authenticating users and managing sessions."""
    def __init__(self):
        #test users-dict
        self.users = {"pekka":User("pekka", "salasana")}

    def login(self, uname, passwd):
        """Logs a user in, sets and returns a session id"""
        if uname not in self.users:
            return None

        user = self.users[uname] #TODO: catch this
        if user.pwhash == bcrypt.hashpw(passwd.encode(), user.salt):
            user.sid = "1" #TODO: something sane here
            return str(user.sid)
        
    def isLogged(self, uname, sid):
        return uname in self.users and sid == self.users[uname].sid
        

    def logout(self, uname, sid):
        print("logout: " + uname + " " + sid)
        if self.isLogged(uname, sid):
            print("should work?")
            self.users[uname].sid = None

    def register(self, uname, passwd):
        if not uname in self.users:
            newUser = User(uname, passwd)
    
    


