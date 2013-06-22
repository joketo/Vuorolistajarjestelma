<p style = "color:green">Kantaan talletetut asiakkaat käynteineen:</p>

<form method="POST" action="/poistaKaynti">
%for a in asiakaslista:
<p>
  <h3>{{a.nimi}}:</h3>
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
