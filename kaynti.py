class Kaynti(object):
    """Asiakaskäyntiin liittyvät tiedot sisältävä olio"""
    def __init__(self, kayntiid, asiakasid, luvat, paiva, aika, kesto):
        self.kayntiid = kayntiid
        self.luvat = luvat
        self.kesto = kesto
        self.aika = aika
        self.paiva = paiva
        self.asiakasid = asiakasid
    
    def __repr__(self):
        return (self.paiva + ", klo " + self.aika + ", " +
                str(self.kesto) + " min")
