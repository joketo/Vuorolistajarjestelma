<p style = "color:green">Kantaan talletetut asiakkaat käynteineen:</p>

<form method="POST" action="/poistaKayntiTaiAsiakas">
%for a in asiakaslista:
<p>
  <h3>{{a.nimi}}:</h3>
  <button name="asiakasid" value ="{{a.asiakasid}}" type="submit">Poista</button>
  %for kaynti in a.kaynnit:
  <ul>
    <li>
        {{kaynti}}
        <button name="kayntiid" value="{{kaynti.kayntiid}}" type="submit">Poista</button>
    </li>        
  </ul>
  %end
</p>
%end
</form>
