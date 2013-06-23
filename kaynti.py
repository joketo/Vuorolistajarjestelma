class Kaynti(object):
    """Simple user info container"""
    def __init__(self, kayntiid, asiakkaat, asiakasid, luvat, paiva, aika, kesto):
        self.kayntiid = kayntiid
        self.luvat = luvat
        self.kesto = kesto
        self.aika = aika
        self.paiva = paiva
        self.asiakasid = asiakasid
        self.asiakkaat = asiakkaat
    
    def kestoNum(self):
        return vakioita.kestot[self.kesto]
    
    def asiakas(self):
        #TODO: arvioi tämän paikka
        return self.asiakkaat.hae(asiakasid=self.asiakasid)

    def __repr__(self):
        return (self.paiva + ", klo " + self.aika + ", " +
                str(self.kesto) + " min")
