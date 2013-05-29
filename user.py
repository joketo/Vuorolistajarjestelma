class User(object):
    """Simple user info container"""
    def __init__(self, userid, name, salt, pwhash):
        self.userid = userid
        self.name = name
        self.salt = salt
        self.pwhash = pwhash
        
