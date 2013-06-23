class Hoitaja(object):
    """Simple user info container"""

    def __init__(self, hoitsuid, nimi, luvat):
        self.hoitsuid = hoitsuid
        self.nimi = nimi
        self.luvat = luvat

    def onkoLuvat(self, luvat):
        """tarkistaa onko annetut luvat"""
        for lupa in luvat:
            if not lupa in self.luvat:
                return False
        return True

    def sopiikoKaynti(self, kaynti):
        return self.onkoLuvat(kaynti.vaatimukset)

    def __repr__(self):
        return self.nimi + " " + str(self.luvat)
