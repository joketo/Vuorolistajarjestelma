%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

%include asiakkaat asiakaslista=asiakkaat
%include lisaaVuoro asiakkaat=asiakkaat
%rebase layout otsikko="Asiakkaiden hallinta"
