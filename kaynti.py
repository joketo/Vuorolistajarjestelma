class Kaynti(object):
    """Simple user info container"""
    def __init__(self, kayntiId, asiakas, vaatimukset, kesto, hoitaja=None):
        self.kayntiId = kayntiId
        self.asiakas = asiakas
        self.vaatimukset = vaatimukset
        self.kesto = kesto
        self.hoitaja = hoitaja

