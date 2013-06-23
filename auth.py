import bcrypt
from bottle import request


class Auth(object):
    """Olio käyttäjien autentikoinnin hallintaan"""
    def __init__(self, userbackend):
        self.users = userbackend

    def login(self, name, password):
        """Kirjaa käyttäjän sisään. Heittää KeyErrorin jos
           tunnus tai salasana eivät kelpaa.
        """
        s = request.environ["beaker.session"]
        user = self.users.byName(name)
        if user.pwhash == bcrypt.hashpw(password.encode(), user.salt):
            s["userid"] = user.userid
            return True
        raise KeyError("Wrong password")

    def loggedAs(self):
        """Palauttaa nimen jolla käyttäjä on loggautunut sisään. 
           Jos käyttäjä ei ole loggautunut, palauttaa None.
        """
        s = request.environ["beaker.session"]

        try:
            user = self.users.byId(s["userid"])
        except KeyError:
            return None
        return user.name

    def isLogged(self):
        """Palauttaa, onko käyttäjä loggautunut sisään vai ei (True/False)"""
        s = request.environ["beaker.session"]
        if "userid" in s:
            return True
        return False

    def logout(self):
        """Kirjaa käyttäjä ulos"""
        s = request.environ["beaker.session"]
        if self.isLogged():
            s.pop("userid")

    def register(self, name, password):
        """Rekisteröi uusi käyttäjä nimen ja salasanan perusteella.
           Käyttäjälle generoidaan suola ja bcrypt(salasana, suola) ja
           nämä tallennetaan tietokantaan.
        """
        salt = bcrypt.gensalt()
        pwhash = bcrypt.hashpw(password.encode(), salt)
        self.users.addUser(name, salt, pwhash)

