class Kaynti(object):
    """Simple user info container"""
    def __init__(self, kayntiid, vaatimukset, paiva, aika, kesto):
        self.kayntiid = kayntiid
        self.vaatimukset = vaatimukset
        self.kesto = kesto
        self.aika = aika
        self.paiva = paiva


