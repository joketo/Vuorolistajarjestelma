%for h in hoitajat:
<p>
  <h3>{{h}}:</h3>
  %for kaynti in hoitajat[h]:
  <ul>
    <li>{{kaynti}}: {{kaynti.asiakas().nimi}}</li>
  </ul>
  %end
</p>
%end
%rebase layout otsikko="Hoitovuorot"
