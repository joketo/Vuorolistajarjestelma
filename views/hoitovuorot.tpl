%for h in hoitajat:
<p>
  <h3>{{h}}:</h3>
  %summa = 0
  %for kaynti in hoitajat[h]:
  <ul>
    %summa = summa + kaynti.kestoNum()
    <li>{{kaynti}}: {{kaynti.asiakas().nimi}}</li>
        
  </ul>
  %end
  
  %tunnit = summa // 60
  %minuutit = summa % 60 
  yht: {{tunnit}} tunti(a) {{minuutit}} minuuttia
</p>
%end
%rebase layout otsikko="Hoitovuorot"
