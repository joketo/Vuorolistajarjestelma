<!--
<table border="2">
<tr>
  <td><b>hoitaja</b></td>
  <td><b>hoidettavat</b></td>  
</tr>
<tr>
%for h in hoitajat:
  <td>{{h}}</td>
  <td>  
%#  {{", ".join([a.nimi for a in hoitajat[h]])}}
  </td>  
</tr>
%end
</table>
-->
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
