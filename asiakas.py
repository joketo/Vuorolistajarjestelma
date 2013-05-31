class Asiakas(object):
    """Simple user info container"""
    def __init__(self, asiakasid, nimi, vaatimukset, kayntiAikaT):
        self.asiakasid = asiakasid
        self.nimi = nimi
        self.vaatimukset = vaatimukset
        self.kayntiAikaT = kayntiAikaT

