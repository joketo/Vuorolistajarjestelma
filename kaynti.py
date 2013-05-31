class Kaynti(object):
    """Simple user info container"""
    def __init__(self, kayntiID, asiakas, vaatimukset, kesto):
        self.kayntiID = kayntiID
        self.asiakas = asiakas
        self.vaatimukset = vaatimukset
        self.kesto = kesto

