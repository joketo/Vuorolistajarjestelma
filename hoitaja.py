class Hoitaja(object):
    """Simple user info container"""
    def __init__(self, hoitsuid, nimi, luvat):
        self.hoitsuid = hoitsuid
        self.nimi = nimi
        self.luvat = luvat
    
    def sopiikoKaynti(kaynti):
        for vaatimus in kaynti.vaatimukset:
            if not vaatimus in self.luvat:
                return False
        return True

        
