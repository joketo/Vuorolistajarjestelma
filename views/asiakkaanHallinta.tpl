%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

%include asiakkaat asiakaslista=asiakkaat
%include lisaaVuoro asiakkaat=asiakkaat, luvat=luvat, paivat=paivat, ajat=ajat, kestot=kestot
%include asiakasKayntiListaus asiakaslista=asiakkaat
%rebase layout otsikko="Asiakkaiden hallinta"
