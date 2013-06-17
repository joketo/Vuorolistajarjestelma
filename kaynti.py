import vakioita


class Kaynti(object):
    """Simple user info container"""
    def __init__(self, kayntiid, asiakasid, luvat, paiva, aika, kesto):
        self.kayntiid = kayntiid
        self.luvat = luvat
        self.kesto = kesto
        self.aika = aika
        self.paiva = paiva
        self.asiakasid = asiakasid
        
    def __repr__(self):
        return (vakioita.paivat[self.paiva] +
                ", klo " + vakioita.ajat[self.aika])
