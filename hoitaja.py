class Hoitaja(object):
    """Säiliöluokka hoitajan tiedoille"""

    def __init__(self, hoitsuid, nimi, luvat):
        self.hoitsuid = hoitsuid
        self.nimi = nimi
        self.luvat = luvat

    def __repr__(self):
        return self.nimi + " " + str(self.luvat)
