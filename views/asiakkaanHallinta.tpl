%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

%include asiakkaat asiakaslista=asiakkaat
%include lisaaVuoro asiakkaat=asiakkaat
%include asiakasKayntiListaus asiakaslista=asiakkaat
%rebase layout otsikko="Asiakkaiden hallinta"
